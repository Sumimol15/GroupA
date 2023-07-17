window.onload=function() {
    var queryString = window.location.search;
    var urlParams = new URLSearchParams(queryString);
    var userId = urlParams.get('userId');
    console.log(userId);
    // const data= GIve data json here
    fetch('/getMyFriends', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(data => {
        // Handle response data
        console.log(data);
      })
      .catch(error => {
        // Handle any errors
        console.error('Error:', error);
      });
};