import goodreads_api_client as gr

client = gr.Client(developer_key='4HBsZgaaX4wIfS5S1TXNtg')

fav_books = ['The Eye of the World', 'Ender''s Game', 'The Path of Least Resistance', '1984', 'Surely You''re Joking, Mr. Feynman']

list_of_suggested_books = []

try:
    for fav_book in fav_books:
        book = client.search_book(fav_book)

        goodreads_id = book['results']['work'][0]['best_book']['id']['#text']

        book = client.Book.show(goodreads_id)

        keys_wanted = ['title', 'similar_books']
        reduced_book = {k: v for k, v in book.items() if k in keys_wanted}

        similar_books = reduced_book['similar_books']['book']

        for item in similar_books:
            # print(item['title_without_series'])
            list_of_suggested_books.append(item['title_without_series'])

except:
    print("Something went wrong")

for s_b in list_of_suggested_books:

    book = client.Book.title(s_b)

    sentiment_raw = book['work']['rating_dist'].split('|')

    # print(sentiment_raw[5].split(':')[1])
    total = float(sentiment_raw[5].split(':')[1])

    percent = 0
    for item in sentiment_raw[:5]:

        current_rating = item.split(':')

        if current_rating[0] == '5':
            percent += ((float(current_rating[1]) / total) * 100)

        elif current_rating[0] == '4':
            percent += ((float(current_rating[1]) / total) * 100)

        else:
            continue

    if percent > 80:
        print(s_b + " : " + str(percent))