St. Louis Salesforce User Group Demo
===========

##### SETUP
```
- Install heroku toolbelt (https://toolbelt.heroku.com/)
- Install git
- Install python 2.7.6
- Install pip (e.g. sudo easy_install pip)
```

```
- Clone our code from github
$ sudo pip install -r requirements.txt (*Note, there are probably excessive requirements leftover in here. You can try installing just the ones you end up needing manually if you'd like)
$ heroku apps:create stl-sf-demo
<you will see a url in your shell. Make it "https", then save it - e.g. https://stl-sf-demo.herokuapp.com/>
```

```
- Create a free developer account on developer.force.com
- Login to Salesforce.
    - Click Setup (top right), then Build->Create->Apps (left side menu).
    - Click "NEW" under Connected Apps.
    - Fill out whatever you want for it's name/etc.
    - Under Canvas App Settings, checkmark the box that says Force.com Canvas.
    - Set Canvas App URL to your heroku URL you saved earlier (ensure https)
    - Ensure Access Method = Signed Request (POST)
    - Also checkmark the box that says "enable oAuth Settings". Use the same url for the callback url, and select "Full Access" for the scope. (We won't really be using this, but Salesforce requires it)
    - Submit.
    - You should now see a Consumer Secret and Consumer Key. In a text editor, open generic_app/settings.py and copy/paste those into SALESFORCE_CONSUMER_KEY and SALESFORCE_CONSUMER_SECRET.
    - Now go back to Salesforce. Go to Setup -> Manage Apps -> Connected Apps. Hit "edit" on your new application. Set permitted users to "Admin Approved users are pre-authorized". While there, set IP Restrictions to "Relax IP Restrictions". Save.
    - Now go to Setup -> Manage Users -> Profiles. Find "System Administrator" (which should be your profile) and hit "Edit". Under "Connected App Access" checkmark your application. Save.
```

```
$ git add .
$ git commit -am 'init'
$ git push heroku master
- On Salesforce, go to Setup -> Canvas App Previewer, then open your app up in the previewer!
```

##### DOCS
[Simple Salesforce (Python Library) Docs](https://pypi.python.org/pypi/simple-salesforce)

[Salesforce SOQL information](http://www.salesforce.com/us/developer/docs/api/index_Left.htm#CSHID=sforce_api_objects_opportunity.htm%7CStartTopic=Content%2Fsforce_api_objects_opportunity.htm%7CSkinName=webhelp)

[Salesforce Object information](http://www.salesforce.com/us/developer/docs/object_reference/object_reference.pdf)
