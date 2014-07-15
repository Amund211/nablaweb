# -*- coding: utf-8 -*-

from django.shortcuts import redirect, get_object_or_404, render
from django.template import loader, Context
from django.contrib.auth.models import User, UserManager
from accounts.forms import UserForm, ProfileForm, RegistrationForm, SearchForm
from accounts.models import UserProfile
from django.contrib import messages
from django.http import HttpResponse, HttpResponsePermanentRedirect

from django.contrib.auth.decorators import login_required

import datetime

## Brukerprofil
@login_required
def view_member_profile(request, username=None):

    """Viser profilen til en oppgitt bruker. Om brukernavn ikke er oppgitt
    vises profilen til brukeren selv."""

    if username:
        member = get_object_or_404(User, username=username)
    else:
        member = request.user
        
    penalty_list = member.eventpenalty_set.all()
   
    see_penalty = request.user.has_perm('bedpress.change_BedPres') or request.user == member
    return render(
        request, "accounts/view_member_profile.html",
        {'member': member, 'penalty_list': penalty_list, 'see_penalty': see_penalty})
    # Render er identisk med render_to_response, men tar request som første
    # argument istedenfor RequestContext(request) som tredje argument.
    # Importeres fra django.shortcuts

from django.views.generic import DetailView


class UserDetailView(DetailView):
    model = User
    template_name = "test.html"


@login_required
def edit_profile(request):
    user = request.user

    userProfile = UserProfile.objects.get_or_create(user=user)[0]

    if request.method == 'GET':
        userForm = UserForm(instance=user)
        profileForm = ProfileForm(instance=userProfile)
    elif request.method == 'POST':
        userForm = UserForm(request.POST, instance=user)
        profileForm = ProfileForm(request.POST, request.FILES, instance=userProfile)
        from pprint import pprint
        pprint(request.FILES)

        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.add_message(request, messages.INFO, 'Profil oppdatert.')
        else:
            messages.add_message(request, messages.ERROR, 'Du har skrevet inn noe feil.')

    return render(request,
        "accounts/edit_profile.html",
        {'userForm': userForm,
          'profileForm': profileForm},
        )


@login_required
def list(request):
    """Lister opp brukere med pagination."""
    users = User.objects.all().prefetch_related('groups')

    return render(request, "accounts/list.html", {'users': users})


@login_required
def search(request):
    """ Returnerer brukerne med brukernavn, fornavn eller etternavn som
        begynner på query """

    from django.db.models import Q

    if not (request.method == 'POST'):
        return HttpResponsePermanentRedirect("/brukere/view")
    
    form = SearchForm(request.POST)
        
    if form.is_valid():
        query = form.cleaned_data['searchstring']

        users = User.objects.filter(Q(username__istartswith=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
        return render(request, "accounts/list.html", {'users': users, 'searchquery': query})
    else:
        return HttpResponsePermanentRedirect("/brukere/view")

def get_name(ntnu_username):
    regex = '^%s:' % username
    process = subprocess.Popen(['grep',regex, settings.NTNU_PASSWD], shell=False, stdout=subprocess.PIPE)
    full_name = process.communicate()[0].split(':')[4].split(" ")
    last_name = full_name.pop()
    first_name = " ".join(full_name)
    return (first_name,last_name)


def user_register(request):
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'] 
            studmail = username+"@stud.ntnu.no"
            (user, created_user) = User.objects.get_or_create(username=username)

            # At en aktivbruker kommer seg hit skal ikke skje. Dette skal skjekkes i forms
            if user.is_active and user.date_joined.date == datetime.date.today():
                raise Exception
            

            if not(user.email):
                user.email = studmail
            user_manager = UserManager()
            password = user_manager.make_random_password()
            user.set_password(password)
            user.is_active = True
            user.save() 
            t = loader.get_template('accounts/registration_email.txt')
            email_text = t.render(Context(locals()))
            user.email_user('Bruker på nabla.no',email_text)

            messages.add_message(request, messages.INFO, 'Registreringsepost sendt til %s' % user.email)

            return redirect('/')
    else:
        form = RegistrationForm()
    
    return render(request,"accounts/user_registration.html",
                               {'form':form}
                               )
