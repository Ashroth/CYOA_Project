function adventure_edit(id)
{
    fetch(`edit/${id}`, {
        method: "PUT",
        body: JSON.stringify({
            title
        })
    })
}