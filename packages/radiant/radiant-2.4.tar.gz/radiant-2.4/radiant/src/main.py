# Generated with django-for-android

""" Start Django in multithreaded mode

It allows for debugging Django while serving multiple requests at once in
multi-threaded mode.

"""

import sys
import os
import time


#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append('Lib')


try:
    from jnius import autoclass
    from radiant.framework.brython.permissions import Permission
    JNIUS = True
except:
    JNIUS = False
    pass

if not '--nodebug' in sys.argv:
    log_path = os.path.abspath("{{APP_LOGS}}")

    if not os.path.exists(log_path):
        os.mkdir(log_path)
        #os.makedirs(log_path, exist_ok=True)

    print("Logs in {}".format(log_path))
    sys.stdout = open(os.path.join(log_path, "stdout.log"), "w")
    sys.stderr = open(os.path.join(log_path, "stderr.log"), "w")

    os.environ['STDOUT'] = os.path.join(log_path, "stdout.log")
    os.environ['STDERR'] = os.path.join(log_path, "stderr.log")


from wsgiref import simple_server

sys.path.append(os.path.join(os.path.dirname(__file__), "{{NAME}}"))

if JNIUS:

    # Create INTENT_FILTERS in environ
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity
    intent = activity.getIntent()
    intent_data = intent.getData()
    try:
        file_uri = intent_data.toString()
        os.environ["INTENT_FILTERS"] = file_uri
    except AttributeError:
        pass


permissions = [getattr(Permission, permission) for permission in {{PERMISSIONS}}]
new_permissions = [permission
                   for permission in permissions
                   if not Permission.check_permission(permission)]

if new_permissions:
    Permission.request_permissions(new_permissions)
    while not Permission.check_permission(new_permissions[-1]):
        time.sleep(0.1)


# ----------------------------------------------------------------------
def django_wsgi_application():
    """"""
    from django.core.wsgi import get_wsgi_application
    print("Creating WSGI application...")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{NAME}}.settings")
    os.environ.setdefault("FRAMEWORK", "django")
    application = get_wsgi_application()
    return application


# ----------------------------------------------------------------------
def brython_wsgi_application():
    """"""
    import static
    print("Creating WSGI application...")
    os.environ.setdefault("FRAMEWORK", "brython")
    from brython_app.{{BRYTHON_MODULE}}.main import {{BRYTHON_CLASS}}
    application = static.Cling(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brython_app'), index_file='index.html', method_not_allowed={{BRYTHON_CLASS}})
    return application


if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brython_app')):
    wsgi_application = brython_wsgi_application
else:
    wsgi_application = django_wsgi_application


if {{APP_MULTITHREAD}}:
    import socketserver

    class ThreadedWSGIServer(socketserver.ThreadingMixIn, simple_server.WSGIServer):
        pass
    httpd = simple_server.make_server('{{IP}}', {{PORT}}, wsgi_application(), server_class=ThreadedWSGIServer)
else:
    httpd = simple_server.make_server('{{IP}}', {{PORT}}, wsgi_application())

httpd.serve_forever()
print("Radiant serving on {}:{}".format(*httpd.server_address))



