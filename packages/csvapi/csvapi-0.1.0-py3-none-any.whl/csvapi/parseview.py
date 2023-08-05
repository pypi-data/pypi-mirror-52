import asyncio
import os
import tempfile

import requests
import validators

from quart import request, jsonify, current_app as app
from quart.views import MethodView

from csvapi.errors import APIError
from csvapi.parser import parse
from csvapi.utils import already_exists, get_executor, get_hash


class ParseView(MethodView):

    async def options(self):
        pass

    async def get(self):
        app.logger.debug('* Starting ParseView.get')
        url = request.args.get('url')
        encoding = request.args.get('encoding')
        if not url:
            raise APIError('Missing url query string variable.', status=400)
        if not validators.url(url):
            raise APIError('Malformed url parameter.', status=400)
        urlhash = get_hash(url)

        def do_parse_in_thread(storage, logger, sniff_limit, max_file_size):
            logger.debug('* do_parse_in_thread %s (%s)', urlhash, url)
            tmp = tempfile.NamedTemporaryFile(delete=False)
            r = requests.get(url, stream=True)
            chunk_count = 0
            chunk_size = 1024
            try:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk_count * chunk_size > max_file_size:
                        tmp.close()
                        raise Exception('File too big (max size is %s bytes)' % max_file_size)
                    if chunk:
                        tmp.write(chunk)
                    chunk_count += 1
                tmp.close()
                logger.debug('* Downloaded %s', urlhash)
                logger.debug('* Parsing %s...', urlhash)
                parse(tmp.name, urlhash, storage, encoding=encoding, sniff_limit=sniff_limit)
                logger.debug('* Parsed %s', urlhash)
            finally:
                logger.debug('Removing tmp file: %s', tmp.name)
                os.unlink(tmp.name)

        if not already_exists(urlhash):
            try:
                storage = app.config['DB_ROOT_DIR']
                await asyncio.get_event_loop().run_in_executor(
                    get_executor(), do_parse_in_thread, storage, app.logger,
                    app.config.get('CSV_SNIFF_LIMIT'), app.config.get('MAX_FILE_SIZE'),
                )
            except Exception as e:
                raise APIError('Error parsing CSV: %s' % e)
        else:
            app.logger.info('{}.db already exists, skipping parse.'.format(urlhash))
        scheme = 'https' if app.config.get('FORCE_SSL') else request.scheme
        return jsonify({
            'ok': True,
            'endpoint': '{}://{}/api/{}'.format(
                scheme, request.host, urlhash
            ),
        })
