function get_signature(method, path, current_user){
    var signature = '';
    var get_data = {
        'method': method,
        'path': path,
        'current_user': current_user
    };
    $.ajax({
        url: '/rest_auth/signature/',
        data: get_data,
        success: function(returned_data){
            signature = returned_data;
        },
        async: false
    });

    return signature
}

// This function is taken from http://stackoverflow.com/questions/6953944/how-to-add-parameters-to-a-url-that-already-contains-other-parameters-and-maybe
function addParameter(url, parameterName, parameterValue){

    replaceDuplicates = true;

    if(url.indexOf('#') > 0){
        var cl = url.indexOf('#');
        urlhash = url.substring(url.indexOf('#'),url.length);
    } else {
        urlhash = '';
        cl = url.length;
    }

    sourceUrl = url.substring(0,cl);



    var urlParts = sourceUrl.split("?");
    var newQueryString = "";

    if (urlParts.length > 1)
    {
        var parameters = urlParts[1].split("&");
        for (var i=0; (i < parameters.length); i++)
        {
            var parameterParts = parameters[i].split("=");
            if (!(replaceDuplicates && parameterParts[0] == parameterName))
            {
                if (newQueryString == "")
                    newQueryString = "?";
                else
                    newQueryString += "&";
                newQueryString += parameterParts[0] + "=" + parameterParts[1];
            }
        }
    }
    if (newQueryString == "")
        newQueryString = "?";
    else
        newQueryString += "&";
    newQueryString += parameterName + "=" + parameterValue;

    return urlParts[0] + newQueryString + urlhash;
}

function update_url_with_signature(method, url){
    var signature = get_signature(method, url, CURRENT_USER);
    url = addParameter(url,'current_user',CURRENT_USER);
    url = addParameter(url,'signed_value',encodeURI(signature));
    return url
}