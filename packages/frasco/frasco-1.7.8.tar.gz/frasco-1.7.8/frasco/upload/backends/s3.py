from flask import current_app, g
from frasco.ext import get_extension_state, has_extension
from frasco.upload.backend import StorageBackend, RemoteOpenStorageBackendMixin
from frasco.upload.utils import save_uploaded_file_temporarly
from frasco.tasks import enqueue_task
import boto
import os


class S3StorageBackend(RemoteOpenStorageBackendMixin, StorageBackend):
    default_options = {'filename_prefix': '',
                       'acl': 'public-read',
                       'async': False,
                       'signed_url': False,
                       's3_urls_ttl': 3600,
                       'set_content_disposition_header_with_filename': True,
                       'ignore_images_content_disposition_header': True,
                       'charset': None,
                       'use_sig_v4': False,
                       'region_name': None,
                       'connect_params': {},
                       'set_contents_headers': {}}

    def save(self, file, filename, force_sync=False):
        kwargs = dict(filename=filename, content_disposition_filename=file.filename,
            bucket=self.options.get('bucket'), acl=self.options['acl'],
            prefix=self.options['filename_prefix'], backend=self.name)

        if not force_sync and self.options.get('async') and has_extension('frasco_tasks'):
            tmpname = save_uploaded_file_temporarly(file, filename)
            enqueue_task(upload_file_to_s3, stream_or_filename=tmpname, mimetype=file.mimetype,
                delete_source=True, **kwargs)
        else:
            upload_file_to_s3(file, **kwargs)

    def url_for(self, filename, **kwargs):
        bucket = self.options.get('bucket')
        if self.options['signed_url']:
            bucket = get_s3_bucket(bucket, self.name)
            bucket_key = bucket.get_key(filename)
            kwargs.setdefault('expires_in', self.options['s3_urls_ttl'])
            return bucket_key.generate_url(**kwargs)
        return 'https://%s.s3.amazonaws.com/%s' % (bucket, filename)

    def delete(self, filename, force_sync=False):
        if not force_sync and self.options['async'] and has_extension('frasco_tasks'):
            enqueue_task('delete_s3_file', filename=filename, backend=self.name)
        else:
            delete_s3_file(filename, backend=self.name)


def get_s3_options(backend=None):
    return get_extension_state('frasco_upload').get_backend(backend or 's3').options


def get_s3_connection(use_cached=True, backend=None):
    if use_cached and "boto_s3_connection" in g:
        return g.boto_s3_connection
    
    options = get_s3_options(backend)
    kwargs = {'aws_access_key_id': options.get('access_key'),
              'aws_secret_access_key': options.get('secret_key')}

    if options.get('use_sig_v4'):
        if not boto.config.get('s3', 'use-sigv4'):
            boto.config.add_section('s3')
            boto.config.set('s3', 'use-sigv4', 'True')
        if options.get('region_name'):
            kwargs['host'] = 's3.%s.amazonaws.com' % options['region_name']
        else:
            kwargs['host'] = 's3.amazonaws.com'

    kwargs.update(options['connect_params'])
    if options.get('region_name'):
        return boto.s3.connect_to_region(options['region_name'], **kwargs)
    conn = boto.connect_s3(**kwargs)
    if use_cached:
        g.boto_s3_connection = conn
    return conn


def get_s3_bucket(bucket=None, backend=None):
    options = get_s3_options(backend)
    if not bucket:
        assert 'bucket' in options, "Missing bucket option"
        bucket = options['bucket']
    try:
        return get_s3_connection(backend=backend).get_bucket(bucket, validate=False)
    except Exception as e:
        current_app.logger.debug(e.body)
        raise


def upload_file_to_s3(stream_or_filename, filename, bucket=None, prefix=None,
                      acl=None, mimetype=None, charset=None, delete_source=False,
                      content_disposition_filename=None, backend=None):
    options = get_s3_options(backend)
    bucket = get_s3_bucket(bucket, backend)
    prefix = prefix or options['filename_prefix']
    bucket_key = bucket.new_key(prefix + filename)
    acl = acl or options['acl']
    headers = {}
    set_content_disposition = options['set_content_disposition_header_with_filename']
    if options['ignore_images_content_disposition_header'] and mimetype and mimetype.startswith('image/'):
        set_content_disposition = False
    if set_content_disposition:
        headers['Content-Disposition'] = 'attachment;filename="%s"' % (
            content_disposition_filename or filename)
    if mimetype:
        headers['Content-Type'] = mimetype
    if charset or options['charset']:
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'binary/octet-stream' # S3 default mimetype
        headers['Content-Type'] += '; charset=%s' % (charset or options['charset'])
    headers.update(options['set_contents_headers'])
    is_filename = isinstance(stream_or_filename, (str, unicode))
    if is_filename:
        bucket_key.set_contents_from_filename(stream_or_filename, headers, policy=acl)
    else:
        bucket_key.set_contents_from_string(stream_or_filename.read(), headers, policy=acl)
    if is_filename and delete_source:
        os.unlink(stream_or_filename)


def delete_s3_file(filename, bucket=None, prefix=None, backend=None):
    options = get_s3_options(backend)
    bucket = get_s3_bucket(bucket, backend)
    prefix = prefix or options['filename_prefix']
    bucket.delete_key(prefix + filename)
