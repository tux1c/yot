from htmlParse import stripTags
import string

import aaFuncs
from wrapLine import wrap



# defines terminal colors for Linux terminals
# used to format 4chan text posts all fancy-like

class TermColor:
	red       = '\033[31m' 
	green     = '\033[32m'
	yellow    = '\033[33m'
	blue      = '\033[34m'
	cyan      = '\033[36m'
	purple    = '\033[35m'
	bold      = '\033[1m'
	reset     = '\033[0m'

def getSpaces(num):
	if num <= 0:
		return ""
	else:
		return " " + getSpaces(num - 1)

def indentText(str, numSpaces):
	sp = getSpaces(numSpaces)
	return sp + string.replace(str, '\n', '\n' + sp)



# takes in a raw text+html comment from a 4chan post
# returns a comment without <span>, <br>, &gt;, etc.; removes them or replaces with color formatting
def cleanCommentData(comment):
	# FIXME bluetext for >>8675309 / >>>/g/7654321 type quotes stays blue until newline;
	#     this affects just posts with body text after >> and >>>
	# FIXME make this take care of [code][/code] and [spoiler][/spoiler] tags
	comment = string.replace(comment, "&gt;&gt;&gt;", TermColor.blue + '>>>')
	comment = string.replace(comment, "&gt;&gt;", TermColor.blue + '>>')
	comment = string.replace(comment, "<br>", '\n' + TermColor.reset)
	comment = string.replace(comment, "&gt;", '>')
	comment = string.replace(comment, "&quot;", '"')
	comment = string.replace(comment, '<span class="quote">', TermColor.green)
	comment = string.replace(comment, '</span>', TermColor.reset)
	comment = stripTags(comment)
	return comment



# takes in an OrderedDict of complete threads
# formats and prints the first post from each thread
# the order threads are printed depends on the order of the thread numbers in threadNumList

def printIndex(index, prefs):
	textWidth = prefs['termWidth']
	replyIndent = prefs['replyIndent']
	imgEnable = prefs['asciiImagesEnable']
	ignoreReplies = prefs['ignoreReplies']
	threadCount = 0

	for thread in index:
		threadCount += 1
		op = thread.getOp()
		opNum = op['no']
		opTimeDate = op['now']
		
		if 'sub' in op:
			opSubject = ' ' + op['sub']
		else:
			opSubject = ""

		textPostsOmitted = ""
		if 'omitted_posts' in op:
			textPostsOmitted += TermColor.blue + str(op['omitted_posts'])
			if op['omitted_posts'] == 1:
				textPostsOmitted += " post "
			else:
				textPostsOmitted += " posts "
			if imgEnable and 'omitted_images' in op:
				if op['omitted_images'] > 0:
					textPostsOmitted += "and " + str(op['omitted_images'])
					if op['omitted_images'] == 1:
						textPostsOmitted += " image reply "
					else:
						textPostsOmitted += " image replies "
			textPostsOmitted += "omitted." + TermColor.reset + "\n"
		
		if 'com' in op:
			opTextRaw = op['com']
			opTextClean = cleanCommentData(opTextRaw)
		else:
			opTextClean = "< no text >"
		
		if imgEnable and 'tim' in op:
			imgUrl = "http://i.4cdn.org/" + thread.getBoard() + "/src/" + str(op['tim']) + op['ext']
			print aaFuncs.urlToAscii(imgUrl, prefs)
		
		print wrap( \
			TermColor.cyan + TermColor.bold + str(threadCount) + ":" + TermColor.yellow + opSubject + TermColor.reset + TermColor.cyan + " No. " + str(opNum) + ' ' + TermColor.purple + opTimeDate + TermColor.reset + '\n' \
			+ opTextClean + '\n' + textPostsOmitted \
			, textWidth)

		if not ignoreReplies:
			for reply in thread.getReplies():
				indent = prefs['replyIndent']
				replyNum = reply['no']
				replyTimeDate = reply['now']

				if imgEnable and 'tim' in reply:
					imgUrl = "http://i.4cdn.org/" + thread.getBoard() + "/src/" + str(reply['tim']) + reply['ext']
					print indentText(aaFuncs.urlToAscii(imgUrl, prefs, indent = True), indent)

				print getSpaces(indent) + TermColor.cyan + "No. " + str(replyNum) + ' ' + TermColor.purple + replyTimeDate + TermColor.reset
			
				if 'com' in reply:
					replyTextRaw = reply['com']
					replyTextClean = cleanCommentData(replyTextRaw)
				else:
					replyTextClean = "< no text >"
			
				print indentText(wrap(replyTextClean, textWidth - indent), indent) + '\n' + TermColor.reset



# takes in a thread in OrderedDict form
# formats and prints all the posts from the given thread

def printThread(thread, prefs):
	textWidth = prefs['termWidth']
	replyIndent = prefs['replyIndent']
	imgEnable = prefs['asciiImagesEnable']
	
	for post in thread:
		postNum = post['no']
		postTimeDate = post['now']

		if imgEnable and 'tim' in post:
			imgUrl = "http://i.4cdn.org/" + thread.getBoard() + "/src/" + str(reply['tim']) + reply['ext']
			print aaFuncs.urlToAscii(imgUrl, prefs)

		print TermColor.cyan + "No. " + str(postNum) + ' ' + TermColor.purple + postTimeDate + TermColor.reset

		if 'com' in post:
			postTextRaw = post['com']
			postTextClean = cleanCommentData(postTextRaw)
		else:
			postTextClean = "< no text >"

		print wrap(postTextClean, textWidth) + '\n' + TermColor.reset
