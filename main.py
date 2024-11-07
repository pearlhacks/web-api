# main.py

from apis import sheets

if __name__ == '__main__':
    schedules = sheets.getSchedule()
    resources = sheets.getResource()
    sponsors = sheets.getSponsor()
    directors = sheets.getDirector()
    faqs = sheets.getFAQ()

    print("Schedules:")
    for schedule in schedules:
        print(schedule)

    print("\nResources:")
    for resource in resources:
        print(resource)

    print("\nSponsors:")
    for sponsor in sponsors:
        print(sponsor)

    print("\nDirectors:")
    for director in directors:
        print(director)

    print("\nFAQs:")
    for faq in faqs:
        print(faq)
