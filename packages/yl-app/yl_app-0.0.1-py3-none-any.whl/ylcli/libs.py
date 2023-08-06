import re
import os


def entry(d, work_path, name):
    text = """from werkzeug.exceptions import HTTPException

    from app import create_app
    from app.libs.error import APIException
    from app.libs.error_code import ServerError

    app = create_app()


    # 整体错误处理
    @app.errorhandler(Exception)
    def framework_error(Exception):
        if isinstance(Exception, APIException):
            return Exception
        elif isinstance(Exception, HTTPException):
            code = Exception.code
            msg = Exception.description
            error_code = 1007
            return APIException(code=code, msg=msg, error_code=error_code)
        else:
            if not app.config['DEBUG']:
                return ServerError()
            else:
                raise Exception


    if __name__ == '__main__':
        app.run(port=app.config['PORT'],
                debug=app.config['DEBUG'], host=app.config['HOST'], threaded=True)
        """
    # 生成项目主文件
    with open(os.path.join(d, 'template', 'YunDou.py'), 'rb') as m:
        text_m = m.read()
    with open(os.path.join(work_path, name + '.py'), 'wb') as f:
        f.write(text_m)
    # 生成Pipfile
    with open(os.path.join(d, 'template', 'Pipfile'), 'rb') as p:
        text_p = p.read()
    with open(os.path.join(work_path, 'Pipfile'), 'wb') as f:
        f.write(text_p)


def other(d, work_path):
    g = os.walk(os.path.join(d, 'template'))
    for path, dir_list, file_list in g:
        # 生成项目目录结构
        for dir_name in dir_list:
            if dir_name != '__pycache__':
                folder = os.path.join(work_path, *re.split(r'[\\/]', path.replace(os.path.join(d, 'template'), '')),
                                      dir_name)
                if not os.path.exists(folder):
                    os.makedirs(folder)

        for file_name in file_list:
            if file_name != 'YunDou.py' and \
                    file_name != 'Pipfile' and \
                    ('.pyc' not in file_name):
                # 原始路径
                origin_file = os.path.join(path, file_name)
                # 当前路径
                current_file = os.path.join(work_path,
                                            *re.split(r'[\\/]', path.replace(os.path.join(d, 'template'), '')),
                                            file_name)
                with open(origin_file, 'rb') as o:
                    origin_text = o.read()
                with open(current_file, 'wb') as c:
                    c.write(origin_text)
