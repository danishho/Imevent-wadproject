function searchEvents() {
    var query = document.getElementById('search-input').value;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/search/?q=' + query, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var events = JSON.parse(xhr.responseText);
            var container = document.getElementById('replaceable-content');
            container.innerHTML = '';
            events.forEach(function(event) {
                var eventCard = document.createElement('a');
                eventCard.className = 'event-card';
                eventCard.href = '/event/' + event.id;

                if (event.image_url) {
                    var img = document.createElement('img');
                    img.src = event.image_url;
                    img.alt = event.title;
                    eventCard.appendChild(img);
                } else {
                    var noImg = document.createElement('p');
                    noImg.textContent = 'No image available.';
                    eventCard.appendChild(noImg);
                }

                var eventInfo = document.createElement('div');
                eventInfo.className = 'event-info';

                var title = document.createElement('h2');
                title.textContent = event.title;
                eventInfo.appendChild(title);

                var location = document.createElement('p');
                var locationIcon = document.createElement('i');
                locationIcon.className = 'fa-solid fa-location-dot';
                locationIcon.style.color = 'red';
                location.appendChild(locationIcon);
                location.appendChild(document.createTextNode(' ' + event.location));
                eventInfo.appendChild(location);

                var date = document.createElement('p');
                var dateIcon = document.createElement('i');
                dateIcon.className = 'fa-regular fa-calendar';
                dateIcon.style.color = 'black';
                date.appendChild(dateIcon);
                date.appendChild(document.createTextNode(' ' + event.start_date + ' - ' + event.end_date));
                eventInfo.appendChild(date);

                var capacity = document.createElement('p');
                capacity.className = 'ticket-status';
                var capacityIcon = document.createElement('i');
                capacityIcon.className = 'fa-solid fa-person';
                capacity.appendChild(capacityIcon);
                capacity.appendChild(document.createTextNode(' ' + event.booked_count + '/' + event.max_tickets));
                if (event.booked_count === event.max_tickets) {
                    capacity.classList.add('full');
                } else {
                    capacity.classList.add('available');
                }
                eventInfo.appendChild(capacity);

                var tagsDiv = document.createElement('div');
                tagsDiv.className = 'tags';
                event.tags.forEach(function(tag) {
                    var tagSpan = document.createElement('span');
                    tagSpan.className = 'tag ' + tag.toLowerCase();
                    tagSpan.textContent = tag;
                    tagsDiv.appendChild(tagSpan);
                });
                eventInfo.appendChild(tagsDiv);

                eventCard.appendChild(eventInfo);
                container.appendChild(eventCard);
            });
        }
    };
    xhr.send();
}
