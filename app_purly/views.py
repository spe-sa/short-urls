from django.shortcuts import render, render_to_response, get_object_or_404
import random, string, json, re, requests, datetime
from app_purly.models import Link
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def redirect_to_home():
    return HttpResponseRedirect('http://www.spe.org/')


@csrf_exempt
def redirect_to_home():
    return HttpResponseRedirect('http://www.spe.org/')


def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('app_purly/index.htm', c)


def multi_match(dic):
    pattern = '^(' + '|'.join(map(re.escape, dic.keys())) + ')'
    return re.search(pattern, lambda m: dic[m.group()])


def multi_replace(dic, txt):
    pattern = '^(' + '|'.join(map(re.escape, dic.keys())) + ')'
    return re.sub(pattern, lambda m: dic[m.group()], txt)


@csrf_exempt
def qr_code(request, data_to_encode='https://v.gd/winlaw', pixels_square='720', format_extension='png', ecc='L'):
    if len(str(data_to_encode)) < 1:
        return None
    api_base = 'http://api.qrserver.com/v1/create-qr-code/'
    referrer = 'http://goqr.me/'
    px = int(pixels_square)  # can range from 150 to 1000
    p = {}
    p['color'] = '223344'  # typical webby RGB in hex
    p['bgcolor'] = 'FBFBFB'  # typical webby RGB in hex
    p['data'] = unicode(data_to_encode)  # or 'https%3A%2F%2Fv.gd%2Fwinlaw'
    p['qzone'] = 1
    p['margin'] = 0
    p['size'] = str(px) + 'x' + str(px)
    p['ecc'] = str(ecc).upper()  # L (Low) is recommended; can be L, M, Q, H
    p['format'] = str(format_extension).lower()  # png is recommended; can be svg, eps, png, jpg
    h = {'Referer': referrer}  # this might not be required anymore
    req = requests.get(api_base, headers=h, params=p)
    res = HttpResponse(req.content)
    res['Content-Type'] = 'image/' + p['format']
    return res


@csrf_exempt
def proxy_get_status_code(from_url, to_url):
    h = {'Referer': from_url}
    r = requests.get(to_url, headers=h, params=t)
    return r.status_code


@csrf_exempt
def triage(request):
    # first we need to combine the requested URI with the HTTP Host header
    # in order to figure out the intended action and be able to do a DB lookup
    u = request.scheme + '://' + request.get_host() + request.get_full_path()

    if re.match('~$', u):
        return HttpResponse(intent + ': @TODO parse out recipient(s)<br />"' + t + '"<br />and then pipe them to the get_link_info() function.  u=<br />"' + u + '"')

    # define how we pluck usernames/mailboxes out of the URL, for when staff wants to get info about a short URL
    email_recipients_regex = r'((,[A-Za-z0-9_-]{1,36}@(spe\.org)?)+)$'  # max 36 chars per mailbox name; all goes in backreference #1

    # define how we grab the right pieces of a URL and use them for real-time QR code generation
    qr_code_images_regex = r'(_([0-9]+)x[0-9]*([LMQH]|\B)\.(png|svg|jpg|eps))$'  # standard image URL suffix; all goes in backreference #1, pixels_square in #2, ECC level in #3, format_extension in #4

    # define what "special" characters we allow for indicating intent
    suffixes_regex = '([:+~\.]|@(spe\.org)?)$'

    if '/' in request.get_full_path():
        p = request.get_full_path()
        short_code_pos = p.rfind('/') + 1
        short_base_choices = re.sub("\('|','[^']+'\)", '', '|'.join(map(re.escape, dict(Link.BASE_CHOICES).keys())))
        # short_base_choices_regex = '^(' + '|'.join(map(str, Link.BASE_CHOICES)) + ')'
        short_base_choices_regex = '^(' + short_base_choices + ')'
        short_base_choices_match = str(re.search(short_base_choices_regex, u).group(0))
        short_base = str(short_base_choices_match)
        # short_base = request.scheme + '://' + request.get_host() + '/' + re.sub(suffixes_regex, '', p[1:short_code_pos])

        # check to see whether or not the request included a verb -- any path portion besides [BASE + CODE]
        after_base = re.sub(suffixes_regex, '', u.replace(short_base, ''))
        if '/' in after_base:
            verb_with_trailing_slash = after_base.split('/')[0] + '/'
            short_code = after_base.split('/')[1]
        else:
            verb_with_trailing_slash = ''
            short_code = re.sub(qr_code_images_regex, '', re.sub(suffixes_regex, '', u.replace(short_base, '')))
        intent_suffix = u.replace(short_base + verb_with_trailing_slash + short_code, '')

    # l = get_object_or_404(Link, short_base=short_base, short_code=short_code)
    try:
        l = Link.objects.get(short_base=short_base, short_code=short_code)
        m = 'Match'
        tu = l.redirect_target_url()
        tt = l.tracking_type
        ttd = l.get_tracking_type_display()
    except Link.DoesNotExist:
        m = 'No matches'
        tu = ''
        tt = ''
    v = verb_with_trailing_slash.replace('/','')
    # intent = 'shorten' if v =='s' else 'redirect' if v =='r' else 'preview' if intent_suffix =='+' else 'check_if_taken' if intent_suffix =='?' else 'admin' if intent_suffix ==':' else 'home' if v=='' and short_code =='' and intent_suffix =='' else 'redirect'
    # so far, this is the closest thing I can find to mimic the simple standard switch/case construct which python lacks
    intent = 'email_link_info' if re.match(email_recipients_regex, p) \
        else 'preview' if intent_suffix == '+' \
        else 'check_if_taken' if intent_suffix == '~' \
        else 'qr_code' if re.match(qr_code_images_regex, after_base.replace(short_code, '')) \
        else 'admin' if intent_suffix == ':' \
        else 'home' if v == '' and short_code == '' and intent_suffix == '' \
        else 'redirect'
    # OK, at this point, we should know the intent and have all the pieces in place to act on it

    if intent == 'check_if_taken':
        return is_short_taken(request, short_base, short_code)

    if intent == 'preview':
        t = l.tracking_string
        tu = l.redirect_target_url()
        l.hit_count += 1
        l.save()

        if tt == 's': # the tracking hit needs to be fired server-side
            t = l.tracking_string
            tu = l.canonical_url
            h = {'Referer': u}
            r = requests.get(tu, headers=h, params=t)
            try:
                rsc = r.status_code
            except:
                rsc = 0
        else: # no need for the server to do anything; either there is no tracking or else the client will do it
            rsc = 0

        c = {} # context object that will be passed to the template
        c['destination_url'] = tu
        c['tracking_type_display'] = str(ttd).lower()
        c['tracking_string'] = t
        c['tracking_hit_status_code'] = rsc
        c['resource_title'] = tu
        c['delay_seconds'] = 7
        return render_to_response('app_purly/interstitial.htm', c)

    if intent == 'qr_code':
        data_to_encode = short_base + short_code
        pixels_square = re.sub(qr_code_images_regex, r'\2', after_base.replace(short_code, ''))
        ecc = '' + re.sub(qr_code_images_regex, r'\3', after_base.replace(short_code, ''))
        format_extension = re.sub(qr_code_images_regex, r'\4', after_base.replace(short_code, ''))
        return qr_code(request, data_to_encode=data_to_encode, pixels_square=pixels_square, format_extension=format_extension, ecc=ecc)

    if intent == 'admin':
        return HttpResponseRedirect('http://go.spe.org/admin/app_purly/link/' + l.short_url_hash + '/')

    if intent == 'redirect':
        # identify whether the short base being used is one that integrates with EVA for event code to be short code
#        domain = re.sub('(^https?://|(:[0-9]+)?/(go/)?$)', '', short_base)
        if short_base == 'http://go.spe.org/' or short_base == 'http://2s.pe/' or short_base == 'http://4s.pe/':
#        if True:

            # identify event codes; use the detail site URL we already have in EVA
            event_code_regex1 = '^(20)?(([0-9]{2})[A-Za-z0-9]{2,4})$' # for easier readability, these two are not combined
            event_code_regex2 = '^([A-Za-z]{2,4})(20)?([0-9]{2})$' # this one catches a few forum edge-case stragglers
            eva_redir_prefix = 'http://eva.spe.org/events/jump/'
            eva_redir_suffix = '?via=' + short_base + short_code

            if re.match(event_code_regex1, short_code) or re.match(event_code_regex2, short_code):
                return HttpResponseRedirect(eva_redir_prefix + short_code + eva_redir_suffix)

        if tt == 'c':
            l.hit_count += 1
            l.save()
            return HttpResponseRedirect(str(l.redirect_target_url()))

        if tt == 's':
            t = l.tracking_string
            u = l.canonical_url
            l.hit_count += 1
            l.save()
            return HttpResponse(intent + ': @TODO conditionally trigger a server-side tracking hit on<br />"' + t + '"<br />and then redirect you to:<br />"' + u + '"')

        if tt == 'n':
            l.hit_count += 1
            l.save()
            return HttpResponseRedirect(str(l.canonical_url))

    if intent == 'email_link_info':
        return HttpResponse(
            intent + ': @TODO parse out recipient(s)<br />"' + t + '"<br />and then pipe them to the get_link_info() function:<br />"' + re.sub(email_recipients_regex, '\1', p) + '"')
        return get_link_info(request,short_code,recipients)

    return HttpResponse('test():<br />\nurl="' + u + '" (' + str(len(u)) + ')<br />\nshort_base_choices_match="' + short_base_choices_match + '"<br />\npath="' + p + '" (' + str(len(p)) + ')<br />base="' + short_base + '" (' + str(len(short_base)) + ')<br />\nverb="' + verb_with_trailing_slash + '"<br />\ncode="' + short_code + '" (' + str(len(short_code)) + ')<br />\nextra="' + intent_suffix + '" (' + str(len(intent_suffix)) + ')<br />\nintent="' + intent + '"<br />\n<br />\n<b>' + m + '</b> found.<br />\ntracking type="' + tt + '"<br />\ntarget URL="' + tu + '"<br />\n')
    # return HttpResponse('test() says: "' + u + '"')


@csrf_exempt
def is_short_taken(request, short_base='', short_code=''):
    # @TODO add some ACAO/ACAM response headers to tell browsers what cross-origin behavior is normal and expected
# # add an indicator of which host (abbreviated) is actually responding to the request
# Header append X-AHA "55k"

# allow cross-domain access (for internal testing/dev purposes; externally, it is invisible anyway)
# SetEnvIf Origin "^(.*\.spe\.org)(:55000)?$" ORIGIN_SAYS=$1
# Header set Access-Control-Allow-Origin "%{ORIGIN_SAYS}e" env=ORIGIN_SAYS
# Header set Access-Control-Allow-Methods "GET, POST, HEAD, OPTIONS"
# Header set Access-Control-Expose-Headers "X-AHA, Etag"

    if short_base == '' or short_code == '':
        u = request.scheme + '://' + request.get_host() + request.get_full_path()

        # @TODO -- verify that this parsing approach still works
        if '/' in request.get_full_path():
            p = request.get_full_path()
            short_code_pos = p.rfind('/') + 1
            short_base = request._get_scheme() + '://' + request.get_host() + '/' + re.sub('[:+~]$', '', p[1:short_code_pos])
            short_code = p[short_code_pos:(len(p) - short_code_pos)]
    else:
        u = short_base + short_code

    try:
        l = [Link.objects.get(short_base=short_base, short_code=short_code)]
        if len(l) == 1:
            who = l[0].pub_user
            til = l[0].end_date
            r = HttpResponse(str(len(l)) + ' match found -- that short URL already exists -- expiration date ' + str(til)[0:10] + ' -- created by ' + who)
            # return r
        else:
            r = HttpResponse(str(len(l)) + ' matches found -- error')
            # return r
    except Link.DoesNotExist:
        r = HttpResponse('0 matches found -- that short URL is available')

    # add some response headers for troubleshooting and for allowing cross-origin requests
    r['X-AHA'] = 't127'
    r['Access-Control-Allow-Origin'] = '*'
    r['Access-Control-Allow-Methods'] = 'GET, POST, HEAD, OPTIONS'
    r['Access-Control-Expose-Headers'] = 'X-AHA, Etag'
    return r


@csrf_exempt
def redirect(request, short_code, short_base_path=''):
    short_base = request._get_scheme() + '://' + request.get_host() + '/' + short_base_path

    l = get_object_or_404(Link, short_base=short_base, short_code=short_code)
    tt = l.tracking_type

    if tt =='c':
        l.hit_count += 1
        l.save()
        return HttpResponseRedirect(str(l.redirect_target_url()))

    if tt == 's':
        t = l.tracking_string
        u = l.canonical_url
        l.hit_count += 1
        l.save()
        return HttpResponse('redirect() wants to trigger a tracking hit on<br />"' + t + '"<br />and then redirect you to:<br />"' + u + '"')

    if tt == 'n':
        l.hit_count += 1
        l.save()
        return HttpResponseRedirect(str(l.canonical_url))


def shorten(request, short_code_requested='', long_url_specified='', tracking_type_specified=''):
    if request.method == 'POST' and request.POST.get("canonical_url", ''):
        canonical_url = request.POST.get("canonical_url", '')
        # TODO: for common bad data entry issues, fail loudly to the user and/or add a bit of pre-insert filtering/trimming/stripping

        tracking_string = request.POST.get("tracking_string", '')
        tracking_type = request.POST.get("tracking_type", '')
        purpose = request.POST.get("purpose", '')
        accounting_code = request.POST.get("accounting_code", '')
        campaign_length_days = int(request.POST.get("campaign_length_days", 18))

        try:
            short_base = request.POST.get("short_base", '')
        except:
            short_base = settings.SITE_URL + '/'

        try:
            short_code = request.POST.get("short_code", '')
        except:
            short_code = get_short_code()

        try:
            pub_user = re.sub('%40', '@', request.COOKIES.get("email", '')) + ' ' + \
                       request.COOKIES.get("first_name", '') + ' ' + \
                       request.COOKIES.get("last_name", '').strip()
        except:
            pub_user = ''

        if short_base != '' and short_code != '' and canonical_url != '':
            end_date = datetime.datetime.now() + datetime.timedelta(days=campaign_length_days);

            n = Link(short_base=short_base, short_code=short_code, canonical_url=canonical_url, tracking_type=tracking_type, tracking_string=tracking_string, purpose=purpose, accounting_code=accounting_code, pub_user=pub_user, end_date=end_date)
            n.save()

            response_data = {}
            response_data['short_url'] = short_base + short_code
            return HttpResponse(json.dumps(response_data),  content_type="application/json")
        return HttpResponse(json.dumps({"error": "debug me"}), content_type="application/json")
    else:
        c = {}
        c.update(csrf(request))
        u = request._get_scheme() + '://' + request.get_host() + request.get_full_path()
        short_base = re.sub('shorten/.+$','',u)
        c['short_base_determined'] = short_base
        try:
            c['current_logged_user_email'] = re.sub('%40', '@', request.COOKIES.get("email", ''))
        except:
            c['current_logged_user_email'] = ''

        if short_code_requested:
            c['short_code_requested'] = short_code_requested.lower()
        if long_url_specified:
            c['long_url_specified'] = long_url_specified
        return render_to_response('app_purly/shorten.htm', c)


def get_link_info(request,short_code,recipients,short_base_path=''):
    short_base = request._get_scheme() + '://' + request.get_host() + '/' + short_base_path

    _r = []
    if ',' in recipients:
        for recipient in recipients.split(','):
            _r.append(recipient)
    else:
        _r.append(recipients)

    short_url = short_base + short_code

    #TODO: check to see that the short URL is valid

    m = Link.objects.filter(short_base=short_base,short_code=short_code)
    c = m.count()
    if c == 0:
        _s = "[purly] Error: " + short_url + " does not exist"
        _t = "No such short URL. The prefix " + short_base + " currently has no short code " + short_code + " defined."
        _h = "<b>No such short URL.</b><br />The prefix &quot;" + short_base + "&quot; currently has no short code &quot;" + short_code + "&quot; defined."
    elif c > 1:
        _s = "[purly] Error: " + short_url + " has multiple matches"
        _t = ""
        _h = ""
    else:
        l = m[0]

#            _r.append(re.sub(' .*$', '', l.pub_user))
        # TODO: sanitize
        # TODO: parse to decide whether this notification is going out via email or twitter

        _s = "[Link Details] " + short_url + ""

        textlines = []
        textlines.append( "Short URL (to be shared): " + short_url )
        textlines.append( "" )
        textlines.append( "Long URL: " + l.canonical_url )
        textlines.append( "Created: " + l.pub_date.strftime("%c") + " by " + l.pub_user )
        if len(l.purpose) > 0: textlines.append( "Purpose: " + l.purpose )
        textlines.append( "Accounting Code: " + l.accounting_code )
        textlines.append( "Tracking Parameters: " + l.tracking_string )
        textlines.append( "Tracking Type: " + l.get_tracking_type_display() )
        if l.hit_count > 0: textlines.append("Hit Count: " + str(l.hit_count) )
        _t = "\n".join(textlines)

        htmllines = []

        short_url_splitter_regex = '^https?://'
        short_url_right = re.sub(short_url_splitter_regex, '', short_url)
        short_url_left = re.sub(short_url_right + '$', '', short_url)
        # htmllines.append( short_url_right )
        # htmllines.append( short_url_left )

        htmllines.append( '<style>BODY { font-size:108%; color:#555; } DD { font-weight:bolder; margin-bottom:1em; color:#222; } A { color:#07b; }</style>' )
        htmllines.append( '<dl>' )
        htmllines.append( '<dt>Short URL (to be shared):</dt><dd>' + short_url_left + '<a style="padding:1px 2px; background:#dfe; color:#070; font-size:198%; text-decoration:none;" href="' + short_url + '">' + short_url_right + '</a></dd>' )
        htmllines.append( '<dt>Long URL:</dt><dd><a href=" + l.canonical_url + ">' + l.canonical_url + '</a></dd>' )
        htmllines.append( "<dt>Created:</dt><dd>" + l.pub_date.strftime("%c") + ' by ' + re.sub(' .*$', '', l.pub_user) + '</dd>' )
        if len(l.purpose) > 0: htmllines.append( "<dt>Purpose:</dt><dd><b>" + l.purpose + '</b>')
        htmllines.append( "<dt>Accounting/EZLabor Code:</dt><dd>" + l.accounting_code + "</dd>" )
        htmllines.append( '<hr />' )
        htmllines.append( "<dt>Tracking Parameters:</dt><dd>" + l.tracking_string + "</dd>" )
        htmllines.append( "<dt>Tracking Type:</dt><dd>" + l.get_tracking_type_display() + "</dd>" )
        if l.hit_count > 0: htmllines.append("<dt>Current Hit Count:</dt><dd>" + str(l.hit_count) )
        htmllines.append( "</dl>" )
        htmllines.append( '<hr />' )
        htmllines.append( '<div align="center"><small style="color:#ccc;"><a href="http://go.spe.org/shorten">purly</a>, the URL shortener and campaign tracking tool</small></div>' )
        _h = "\n".join(htmllines)

    _f = '"purly" <noreply@spe.org>'

    if "@" in recipients:
        successfully_delivered_messages = send_mail(_s, _t, _f, _r, fail_silently=False, auth_user=None, auth_password=None,
              connection=None, html_message=_h)
        return HttpResponse(json.dumps({"successfully_delivered_messages": successfully_delivered_messages, "recipients": recipients }),
                            content_type="application/json")
    else:
        return HttpResponse("<h1>purly</h1><h2>Link Details</h2>" + _h, content_type="text/html")




def get_short_code():
    length = 7
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while True:
        short_code = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Link.objects.get(pk=short_code)
        except:
            return short_code
