import os
import zipfile

from django.conf import settings
from django.http import StreamingHttpResponse, HttpResponse
from django.views import View

from comk_django_plugin import PublicServer


class GetLog(View):
    '''
    获取日志
    '''

    def get(self, request, log_name):

        ps = PublicServer(request)
        check_result = ps.check_login_user()
        if not check_result:
            return ps.return_build_error_response(msg='未登录，请先通过django-admin进行登录')

        user = request.user
        if not user.is_superuser:
            return ps.return_build_error_response(msg='您不是超级用户，无法下载文件')

        BASE_DIR = settings.BASE_DIR
        log_dir = '{}/log'.format(BASE_DIR)
        if log_name == 'log_download_html':
            log_file_names = [f for f in os.listdir(log_dir) if
                              'log' in f and 'zip' not in f and os.path.isfile(os.path.join(log_dir, f))]
            return HttpResponse(self.build_flies_html(request, log_file_names, log_name))
        elif log_name == 'log.zip':
            # 生成压缩文件
            os.chdir(log_dir)
            self.compress_file(log_name, '.')
            the_file_name = "{}/{}".format(log_dir, log_name)
            response = StreamingHttpResponse(self.file_iterator(the_file_name, mode='rb'))
            response['Content-Type'] = 'application/zip'
        else:
            the_file_name = "{}/{}".format(log_dir, log_name)
            if not (os.path.exists(the_file_name)):  # 对该是否存在，进行判定。
                return ps.return_build_error_response(msg='{}文件不存在'.format(log_name))

            response = StreamingHttpResponse(self.file_iterator(the_file_name, encoding='utf-8'))
            response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(log_name)
        return response

    def build_flies_html(self, request, log_file_names, log_name):
        '''
        构建下载文件的链接

        :param request:
        :param log_file_names:
        :param log_name:
        :return:
        '''
        url_path = request.path

        flies_html = '''
           日志文件：<br>
           <a href="{}">下载所有日志文件的压缩包</a>
           <br><br>
           '''.format(url_path.replace(log_name, 'log.zip'))
        for log_file_name in log_file_names:
            href = url_path.replace(log_name, log_file_name)
            flies_html += '<a href="{}">{}</a><br>'.format(href, log_file_name)
        return flies_html

    def compress_file(self, zipfilename, dirname):  # zipfilename是压缩包名字，dirname是要打包的目录
        '''
        压缩所有的log文件

        :param zipfilename:
        :param dirname:
        :return:
        '''
        if os.path.isfile(dirname):
            with zipfile.ZipFile(zipfilename, 'w') as z:
                z.write(dirname)
        else:
            with zipfile.ZipFile(zipfilename, 'w') as z:
                for root, dirs, files in os.walk(dirname):
                    for single_file in files:
                        if single_file != zipfilename:
                            filepath = os.path.join(root, single_file)
                            z.write(filepath)

    def file_iterator(self, file_name, chunk_size=512, mode='r', encoding=None):
        '''
        下载文件

        :param file_name:
        :param chunk_size:
        :return:
        '''
        with open(file_name, mode, encoding=encoding) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
