# **MetaScraper**

### When you're too lazy to click through 100 links and spam 100 commands.

![HereWeGo](https://media.giphy.com/media/YPIrsRqqO7oB2/giphy.gif)

> _“Do I really look like a guy with a plan? You know what I am? I'm a dog chasing cars. I wouldn't know what to do with one if I caught it! You know, I just... **do** things.”_
>
>_- Heath Ledger_

If you haven't noticed, there's a recurring theme here but there is a method to the madness.

___

#### A quick note on this tool.

There is a limit of 100 results on any query from Google's API, so there is a limit of 100 to this tool, as well. Just a fair warning that there could be thousands of results, but this will still get only 100. (Working on a solve for this for later, but you can work around this by narrowing searches and just increasing the number you make, if really necessary.)

___

### Why develop this?

___

One very important portion of a pentest is the Open Source Intelligence (OSINT) gathering. What some people may not know, however, is just how valuable online posts in the company's name can be. For example, an employee may have their author information set on a pdf they write and upload to the site. Now, that PDF's metadata has their contact information (and if they are really careless, it could be personal email or phone number). A less common, but still possible situation is when the PDF contains the upload location, which could also be the IP of the machine.

In both of these cases, a pentester has used access to PDF metadata that was openly available on the web to gain access to previously unknown information that can be leveraged, whether using the personal information for Social Engineering or the device intelligence for setting up an attack vector.

With this knowledge in mind ~~(and me being **lazy**)~~, I wanted a way to be able to discover these PDFs and dump the metadata out to a location in a way in which I could analyze it and find important information **WITHOUT NEEDING TO DOWNLOAD AND EXAMINE ONE BY ONE**.

I put that in caps because when I first had to do this I did a search and discovered over a hundred results that we wanted to examine for our test and then spent an inordinate amount of time "HandJamming" it, to put it like my calculus teacher (*shudder*). Suffice to say - I did not want to do that ever again.
___
### So that's where this tool came in.
___
What would be the best way to get the results from a google query and then grab the urls of the results? Luckily there's this great, if slightly annoying, tool called the Custom Search Engine (CSE) API.

The steps involved here are pretty simple, too (at least for you, now).

#### 1) Set up your CSE

For instructions on setting up your personal CSE check this [link](https://support.google.com/customsearch/answer/2630963?hl=en) out. The free edition is perfectly fine and make sure to use the dropdown menu on "Sites to search" to set the search to "Search the entire web".

#### 2) Set up your API Account

As for the API Key. You will need to set up your API account, create a project, then get your API code to use. Sorry I redact mine, but you only get so much credit and I really don't want to pay for someone else's searches!

Here is a [short guide](https://support.google.com/cloud/answer/6158862?hl=en) to set up the API, I used the Custom Search Engine v1. If you stick with the free account, you will only be allowed 100 queries per day, which is more than enough for a small project, but the free trial gives you two months of access and $300 of credit- so that's pretty cool too.

#### You're ready to go!

I put my API key and CSE cv code into a simple text file called `API_Key.txt` and `SE_Code.txt` in the same folder as the python file so that they could be read and used in the program and I could just .gitignore them and not share my precious keys (honestly I could probably share the CSE, but for the sake of saying I'm paranoid?).
