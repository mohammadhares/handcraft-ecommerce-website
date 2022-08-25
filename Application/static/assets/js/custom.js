function doDelete(msg)
{
    var ans = confirm(msg);
    if(!ans)
        event.preventDefault();
}