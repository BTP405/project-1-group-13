from django.shortcuts import render, redirect
from .utils import supabase_client
import uuid


#TODO create a view that renders an html file / page for adding a contact. This should be a form 
# that looks similar to the update page. The button for adding a contact should be on the home page.
# Include a button on your 'add contact' page that can take you back to the home page. You can create the
# html page in the 'base/templates/base' folder (RIYA). Ensure that you add your route in the 'urls.py' file. 

#TODO create a modal window that appears when the 'delete contact' button is clicked. This button can
# be found on the 'update' page. The modal window will confirm if the user wants to delete the contact
#(achieve this by utilizing the contact_id of the contact). if the user chooses yes, delete the contact. 
# the database was created so that the associated phone and social_media information will be deleted if 
# their associated contact is deleted. So just delete the contact. do not worry about deleting the phone 
# and social_media. (Kabir)

#TODO make this thing look pretty (Kabir)


#use this function to retrieve all the data. 
def getData(pk): 
    #will retrieve the information from the CONTACTS table
    contactResponse = supabase_client.from_('contacts').select('*').eq('contact_id', pk).execute()
    conactData = contactResponse.data
    contactInfo = conactData[0] # This is an array that contains the contact with the contact_id that is equal to 'pk'
                                # since all the contact_id's are unique, there will onlt be one that matches with 
                                # 'pk'. Therefore we only need to access the one in the first index.  
    
    #will retrieve the information from the PHONE table
    phoneResponse = supabase_client.from_('phone').select('*').eq('contact_id', pk).execute()
    phoneData = phoneResponse.data
    phoneInfo = phoneData[0]# This is an array that contains the phone with the contact_id that is equal to 'pk'
                            # since all the contact_id's are unique, there will onlt be one that matches with 
                            # 'pk'. Therefore, we only need to access the one in the first index.  
    
    
    #will retrieve the information from the SOCIAL_MEDIA table
    socialsResponse = supabase_client.from_('social_media').select('*').eq('contact_id', pk).execute()
    socialData = socialsResponse.data
    socialInfo = socialData[0] # This is an array that contains the social_media with the contact_id that is equal to 'pk'
                                # since all the contact_id's are unique, there will onlt be one that matches with 
                                # 'pk'. Therefore we only need to access the one in the first index.  
    
    
    allData = [contactInfo, phoneInfo, socialInfo] #stores everything in an array which will be accessed in the following code
                                                    #allData[0] = contactInfo, allData[1] = phoneInfo, allData[2] = socialInfo
    
    return allData

def home(request): 
    data, error = supabase_client.from_('contacts').select('*').execute()
    return render(request, 'base/home.html', {'data': data})

# Render all of the information about a person based on their contact_id
def person(request, pk):

    allData = getData(pk) # gets all contact, phone, and socials information
    
    return render(request, 'base/person.html', {'person': allData[0], 'phone': allData[1], 'socials': allData[2]})
                                                # Indexing is used to assign the key with the value that is stored in 
                                                # the specefied index
                                                
#update all of the information about a person based on their contact_id
def update(request, pk):
    allData = getData(pk)
    
    if request.method =='POST': 
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        notes = request.POST.get('notes')
        address = request.POST.get('address')
        birthday = request.POST.get('birthday')
        
        work = request.POST.get('work')
        school = request.POST.get('school')
        home = request.POST.get('home')
        mobile = request.POST.get('mobile')
        other = request.POST.get('other')
        
        instagram = request.POST.get('instagram')
        twitter = request.POST.get('twitter')
        facebook = request.POST.get('facebook')
        discord = request.POST.get('discord')
        other = request.POST.get('other')
        
        
        updatedContactInfo = {
            'fname': fname,
            'lname': lname,
            'email': email,
            'notes': notes,
            'address': address,
            'birthday': birthday,
        }
        
        updatedPhoneInfo = {
            'work' : work,
            'school' : school,
            'home' : home,
            'mobile' : mobile,
            'other' : other
        }
        
        updatedSocialsInfo = {
            'instagram': instagram, 
            'twitter' : twitter, 
            'facebook' : facebook, 
            'discord' : discord, 
            'other' : other,
        }
        
        supabase_client.from_('contacts').update(updatedContactInfo).eq('contact_id', pk).execute()
        supabase_client.from_('phone').update(updatedPhoneInfo).eq('contact_id', pk).execute()
        supabase_client.from_('social_media').update(updatedSocialsInfo).eq('contact_id', pk).execute()
        return redirect('person', pk=pk )
    
    return render(request, 'base/update.html', {'contactInfo': allData[0], 'phoneInfo' : allData[1], 'socialInfo' : allData[2]} )

#TODO RIYA 
def add(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        notes = request.POST.get('notes')
        address = request.POST.get('address')
        birthday = request.POST.get('birthday')

        work = request.POST.get('work')
        school = request.POST.get('school')
        home = request.POST.get('home')
        mobile = request.POST.get('mobile')
        otherPhone = request.POST.get('other')

        instagram = request.POST.get('instagram')
        twitter = request.POST.get('twitter')
        facebook = request.POST.get('facebook')
        discord = request.POST.get('discord')
        otherSocial = request.POST.get('other')

        contact_id = str(uuid.uuid4())

        contact_info = {
            'contact_id': contact_id,
            'fname': fname,
            'lname': lname,
            'email': email,
            'notes': notes,
            'address': address,
            'birthday': birthday,
        }

        phone_info = {
            'contact_id': contact_id,
            'work': work,
            'school': school,
            'home': home,
            'mobile': mobile,
            'other': otherPhone
        }

        socials_info = {
            'contact_id': contact_id,
            'instagram': instagram,
            'twitter': twitter,
            'facebook': facebook,
            'discord': discord,
            'other': otherSocial
        }

        supabase_client.from_('contacts').insert(contact_info).execute()

        supabase_client.from_('phone').insert(phone_info).execute()

        supabase_client.from_('social_media').insert(socials_info).execute()

        return redirect('person', pk=contact_id)
    
    return render(request, 'base/add.html')


def delete_contact(request, pk):
    if request.method == 'POST':
        # Perform the deletion operation in the database
        supabase_client.from_('contacts').delete().eq('contact_id', pk).execute()
        # Redirect the user to the home page or another appropriate page
        return redirect('home')
    # Render the delete confirmation modal template
    return render(request, 'base/delete_confirm.html', {'pk': pk})


        


