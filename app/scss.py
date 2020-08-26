import os
import click


def register(app):
    @app.cli.group()
    def scss():
        """SCSS compiler // Please do not change the location of the bootstrap-4.5.0 folder"""
        pass

    @scss.command()
    def compile():
        """Compile Bootstrap SCSS."""
        if os.system('sass app/static/scss/bootstrap-4.5.0/scss/bootstrap.scss app/static/bootstrap/css/bootstrap.min.css --style compressed'):
            raise RuntimeError('compile command failed')

    @scss.command()
    def compile_watch():
        """Compile Bootstrap SCSS."""
        if os.system('sass --watch app/static/scss/bootstrap-4.5.0/scss/bootstrap.scss app/static/bootstrap/css/bootstrap.min.css --style compressed'):
            raise RuntimeError('compile command failed')