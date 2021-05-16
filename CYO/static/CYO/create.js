function adventure_edit(id)
{
    fetch(`edit/${id}`, {
        method: "PUT",
        body: JSON.stringify({
            title
        })
    })
}

function adventure(event_id)
{
    fetch(`event/${event_id}`,{
        method: 'GET'
    })
    .then((response) => response.json())
    .then((response) => {
        if (response.status == 404)
        {
            return null;
        }
        let title = document.querySelector("#title");
        let text = document.querySelector("#text");
        title.innerHTML = `<h3>${response.title}</h3>`;
        text.innerHTML = response.text;
        text.innerHTML += '\n';
        for (i in response.choices)
        {
            let choice = response.choices[i]
            let choice_element = document.createElement('button');
            choice_element.setAttribute('onclick', `adventure('${choice[0]}')`);
            choice_element.innerHTML = choice[1];
            text.append(choice_element)
        }
    });
}