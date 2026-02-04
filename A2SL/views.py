from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required

def home_view(request):
	return render(request,'home.html')


def about_view(request):
	return render(request,'about.html')


def contact_view(request):
	return render(request,'contact.html')

@login_required(login_url="login")
def animation_view(request):
	if request.method == 'POST':
		text = request.POST.get('sen', '').strip()
		
		# Validate input
		if not text:
			return render(request,'animation.html',{'error': 'Please enter some text or use the microphone.'})
		
		try:
			#stopwords that will be removed
			stop_words = set(["mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', "you've",'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", "wasn't", 'its', "haven't", "wouldn't", 'don', 'weren', 's', "you'd", "don't", 'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the', 'mustn', 'i', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have',  'hasn', 'o', "aren't", "you'll", "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 'an', 'hadn', 'whom', 'y', "hasn't", 'itself', 'couldn', 'needn', "shan't", 'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did', 'ma', 't', 'having', 'mightn', 've', "isn't", "won't"])

			try:
				#tokenizing the sentence
				text_lower = text.lower()
				#tokenizing the sentence
				words = word_tokenize(text_lower)

				tagged = nltk.pos_tag(words)
				tense = {}
				tense["future"] = len([word for word in tagged if word[1] == "MD"])
				tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
				tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
				tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])

				#removing stopwords and applying lemmatizing nlp process to words
				lr = WordNetLemmatizer()
				filtered_text = []
				for w,p in zip(words,tagged):
					if w not in stop_words:
						if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
							filtered_text.append(lr.lemmatize(w,pos='v'))
						elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
							filtered_text.append(lr.lemmatize(w,pos='a'))

						else:
							filtered_text.append(lr.lemmatize(w))

				#adding the specific word to specify tense
				words = filtered_text
				temp=[]
				for w in words:
					if w=='I':
						temp.append('Me')
					else:
						temp.append(w)
				words = temp
				probable_tense = max(tense,key=tense.get)

				if probable_tense == "past" and tense["past"]>=1:
					temp = ["Before"]
					temp = temp + words
					words = temp
				elif probable_tense == "future" and tense["future"]>=1:
					if "Will" not in words:
							temp = ["Will"]
							temp = temp + words
							words = temp
					else:
						pass
				elif probable_tense == "present":
					if tense["present_continuous"]>=1:
						temp = ["Now"]
						temp = temp + words
						words = temp
				
			except Exception as e:
				# Fallback if NLTK data is missing or other NLTK error
				print(f"NLTK Processing failed, using fallback: {e}")
				words = text.lower().split()
				
				# Remove stop words manually
				words = [w for w in words if w not in stop_words]
				
				# Basic replacements
				for i in range(len(words)):
					if words[i] == 'i':
						words[i] = 'Me'

			# Final processing for video paths - runs for both success and fallback
			filtered_text = []
			for w in words:
				path = w + ".mp4"
				f = finders.find(path)
				
				# Try Capitalized match if exact fails
				if not f:
					path = w.capitalize() + ".mp4"
					f = finders.find(path)
				
				#splitting the word if its animation is not present in database
				if not f:
					for c in w:
						filtered_text.append(c)
				#otherwise animation of word
				else:
					# Use the capitalized version if that's what we found, or the original
					if finders.find(w.capitalize() + ".mp4"):
						filtered_text.append(w.capitalize())
					else:
						filtered_text.append(w)
			words = filtered_text;


			return render(request,'animation.html',{'words':words,'text':text})
		
		except Exception as e:
			# Catch any other unexpected errors
			print(f"Error processing text: {e}")
			import traceback
			traceback.print_exc()
			return render(request,'animation.html',{'error': 'An error occurred while processing your text. Please try again.'})
	else:
		return render(request,'animation.html')




def signup_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request,user)
			# log the user in
			return redirect('animation')
	else:
		form = UserCreationForm()
	return render(request,'signup.html',{'form':form})



def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			#log in user
			user = form.get_user()
			login(request,user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				return redirect('animation')
	else:
		form = AuthenticationForm()
	return render(request,'login.html',{'form':form})


def logout_view(request):
	logout(request)
	return redirect("home")
