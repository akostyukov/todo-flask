from flask import render_template, request, redirect, url_for
from flask.views import MethodView


class FormView(MethodView):
    form = None
    template = ''
    success_url = ''
    fail_url = ''

    def get_context(self):
        return {}

    def get(self):
        return render_template(self.template, form=self.form(), **self.get_context())

    def post(self):
        form = self.form(request.form)

        if form.validate_on_submit():
            try:
                form.save()
            except:
                return redirect(url_for(self.fail_url))
            else:
                return redirect(url_for(self.success_url))
