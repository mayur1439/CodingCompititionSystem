from django import forms

class PasswordChangeForm(forms.Form):
	old_password = forms.CharField(label="id_old_password",widget=forms.PasswordInput(render_value=False))
	new_password1=forms.CharField(label="id_new_password1",max_length=12,widget=forms.PasswordInput(render_value=False))
	new_password2=forms.CharField(label="id_new_password2",max_length=12,widget=forms.PasswordInput(render_value=False))

	def clean(self):
		if self._errors:
			return
		user = auth.authenticate(**self.user_credentials())
		if user:
			if user.is_active:
				self.user = user
			else:
				raise forms.ValidationError(_("This account is inactive."))
		else:
			raise forms.ValidationError(self.authentication_fail_message)
			return self.cleaned_data
