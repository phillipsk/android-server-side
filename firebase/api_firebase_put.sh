




#curl -i -X PUT -d '{"content": "Everyone is Invited!", "content_type": "image", "description": "Description", "likes": "120", "photo": "https://scontent.fbed1-2.fna.fbcdn.net/v/t1.0-9/118776668_3956515624365393_3218013440126320767_n.jpg?_nc_cat=103&_nc_sid=8024bb&_nc_ohc=TvAXorV7YsYAX85IPzb&_nc_ht=scontent.fbed1-2.fna&oh=6e65f30e6524d8e3dabd876292830397&oe=5F74B746", "title": "Everyone is Invited!"}' \
# 'https://fmc1fmc2.firebaseio.com/announcements.json'



curl -vX PUT https://fmc1fmc2.firebaseio.com/announcements.json \
  -d @api_firebase.json \
  --header "Content-Type: application/json" \
  -o post_response.txt