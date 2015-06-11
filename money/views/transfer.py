from django.views.generic import CreateView
from money.forms import TransferForm

class TransferCreate(CreateView):
    form_class = TransferForm
    template_name = 'money/transfer_create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TransferCreate, self).form_valid(form)
