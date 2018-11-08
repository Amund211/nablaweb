from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django import forms
from django.core.exceptions import ValidationError

from .models import Account, Transaction, Product, DepositRequest
from datetime import datetime

class AccountView(TemplateView):
    template_name = "officeBeer/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Todo what if user does not have an account? Is get_or_create appropriate fix?
        context['account'] = Account.objects.get_or_create(user=self.request.user)[0]
        context['transaction_list'] = Transaction.objects.filter(account=context['account'], amount__lt=0)
        context['deposit_list'] = Transaction.objects.filter(account=context['account'], amount__gt=0)
        return context

class PurchaseForm(forms.Form):
    product = forms.ChoiceField(widget=forms.RadioSelect)
    user_card_key = forms.CharField(label="Kortnummer",
                                    widget=forms.TextInput(attrs={'placeholder': 'Scan kort', 'autofocus':'true'}))


    # Could use ModelChoiceField for product, but this would require to
    # subclass ModelChoiceField to override label_from_instance method.
    # https://docs.djangoproject.com/en/2.1/ref/forms/fields/#modelchoicefield
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        products = Product.objects.all()
        
        self.fields['product'].choices=[(p.id, f"{p.name} - {p.price}kr") for p in products]
        self.fields['product'].widget.option_template_name = "officeBeer/radio_option.html"

    # todo valid product
    def clean_user_card_key(self):
        data = self.cleaned_data['user_card_key']

        # Check that there is an account with the given card key
        if not Account.objects.filter(user__ntnu_card_number=data).exists():
            raise ValidationError(f'There are no registered accounts with card key {data},\
                                    the user might not have registered their key card or \
                                    does not have an account for officebeer')
        return data

class DepositRequestForm(forms.Form):
    """ 
    Form to register when you have deposited money. The admin has to approve the request
    """

    amount = forms.IntegerField()
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
class PurchaseView(TemplateView):
    template_name = "officeBeer/purchase.html"

    def post(self, request, *args, **kwargs):
        purchase_form = PurchaseForm(request.POST)
        
        if purchase_form.is_valid():
            account = Account.objects.get(user__ntnu_card_number=purchase_form.cleaned_data['user_card_key'])
            product_id = purchase_form.cleaned_data['product']
            product = Product.objects.get(id=product_id)
            price = product.price
            account.balance -= price

            Transaction(description=f"{price}NOK from {account.user.username}'s account for {product.name}",
                        amount=-price,
                        account=account,
                        date=datetime.now()).save()
            account.save()

            return redirect(self.request.resolver_match.view_name)
        
        context = {
            'form' : purchase_form
        }

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PurchaseForm()
        return context

class DepositRequestView(TemplateView):
    template_name = "officeBeer/deposit.html"

    def post(self, request, *args, **kwargs):
        deposit_form = DepositRequestForm(request.POST)

        if deposit_form.is_valid():
            account = Account.objects.get(user=request.user)

            DepositRequest(account=account, amount = deposit_form.cleaned_data['amount']).save()

            return redirect(self.request.resolver_match.view_name)
            
    # def form_valid(self, form):
    #     account = Account.objects.get(user=form.cleaned_data['user'])
    #     DepositRequest(account=account, amount=form.cleaned_data['amount']).save()
    #     super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DepositRequestForm(user=self.request.user)
        return context
