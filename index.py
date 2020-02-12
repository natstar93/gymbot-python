import asyncio
import sys
from pyppeteer import launch

username = 'natalie.akam@gmail.com'
password = 'Y8GJY5a2'

async def main():
    # print('\nsys.argv', sys.argv)
    
    # _, username, password, classId = sys.argv

    username = 'natalie.akam@gmail.com'
    password = 'Y8GJY5a2'
    classId = 'slot1212049'
    
    # print('\n_', _)
    print('\nclassId', classId)
    
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://gymbox.legendonlineservices.co.uk/enterprise/account/login')

    await page.waitFor('input[name="login.Email"]')
    
    await page.focus('input[name="login.Email"]')
    element = await page.querySelector('input[name="login.Email"]')
    await element.type(username)

    await page.focus('input[name="login.Password"]')
    element = await page.querySelector('input[name="login.Password"]')
    await element.type(password)

    await page.screenshot({'path': 'screenshots/example.png'})
 
    print('\nEntering login details')
    
    await page.click('input[type="submit"]')

    try:
        await page.waitFor('.fieldSetContent')
    except Exception:
        print('\nFailed to login')
        return
  
    await page.goto('https://gymbox.legendonlineservices.co.uk/enterprise/BookingsCentre/MemberTimetable')

    await page.screenshot({'path': 'screenshots/example1.png'})

    await page.waitFor('table#MemberTimetable')

    await page.screenshot({'path': 'screenshots/example2.png'})
    
    await page.select('select', 'MemberTimetable?clubId=4')
    
    await page.screenshot({'path': 'screenshots/example2.5.png'})
    
    print('\nAdding {0} to basket'.format(classId))

    try:
        await page.click('a#{0}'.format(classId))
    except Exception:
        await page.screenshot({'path': 'screenshots/example3.png'})
        print('\nCould not find class {0}'.format(classId))
        return

    await page.screenshot({'path': 'screenshots/example3.5.png'})
    
    try:
        print('\nWaiting for basket')
        await page.waitFor('div.basketButtonWrapper')
    except Exception:
        print('\nBasket page not loaded. Trying to book waiting list {0}'.format(Exception))
        print('\npage.frames[1]', page.frames[1].name)
        modal = page.frames[1]
        values = await modal.evaluate('''() => [...document.querySelectorAll('div')].map(element => element.className)''')
        print('\nvalues', values)
        # await page.screenshot({'path': 'screenshots/example4.png'})
        # await page.click('div.formSubmit a')
        return
        # 
        # 


        # try:
        #   await page.waitFor('div.formSubmit a:first-child')
        #   await page.click('div.formSubmit a:first-child')
        #   return 
        # except Exception:
        #   print('\nWaiting list modal not loaded')

        # try:
        #     frames = await page.frames()
        #     await page.screenshot({'screenshots/path': 'example5.png'})
        #     # await page.waitFor('div.formSubmit a:first-child')
        #     # await page.click('div.formSubmit a:first-child')
        # except Exception:
        #     print('\nframes crapped out {0}'.format(Exception))
        #     return    

    await page.waitFor('a#btnPayNow')
    await page.click('a#btnPayNow')

    await page.waitFor('https://gymbox.legendonlineservices.co.uk/enterprise/basket/paymentconfirmed')

    print('\nClass booked!')

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())