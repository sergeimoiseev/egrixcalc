# -*- coding: utf-8 -*-
import flask, flask.views
import calc_tools as ct
import params_processor as proc
import logging

logger = logging.getLogger(__name__)

app = flask.Flask(__name__)
app.debug = True
app.secret_key = "bacon"

default_params, params_comments = ct.get_and_store_params(load_from_dropbox=True)

class Main(proc.EgrixCalcView):
    def get(self):
        return flask.render_template('index.html',d = default_params, c = params_comments)

    def post(self):
        logger.info("post request in Main")

        messages_to_flash, html_path = self.process_params('index')
        
        logger.info("html_path\n%s" % (html_path,))
        flask.flash(messages_to_flash[0])
        flask.flash(messages_to_flash[1])

        return flask.redirect(flask.url_for('index'))

class AllParams(proc.EgrixCalcView):
    def get(self):
        global default_params, params_comments
        return flask.render_template('all_params.html',d = default_params, c = params_comments)

    def post(self):
        logger.info("post request in AllParams")

        messages_to_flash, html_path = self.process_params('all_params')
        logger.info("html_path\n%s" % (html_path,))
        flask.flash(messages_to_flash[0])
        flask.flash(messages_to_flash[1])

        return flask.redirect(flask.url_for('all_params'))

app.add_url_rule('/',
        view_func=Main.as_view('index'),
        methods=['GET', 'POST'])

app.add_url_rule('/all_params/', 
        view_func=AllParams.as_view('all_params'),
        methods=['GET', 'POST'])

if __name__ == '__main__':
    ct.setup_logging()
    app.run()