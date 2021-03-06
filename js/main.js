const deploy = async () => {
    // get form values
    const text_book = document.getElementById('text_book').value;
    const slider_val = document.getElementById('myRange').value;
    console.log(text_book);
    // store voter information in local database
    fetch("/", {
        credentials: 'same-origin',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          "text_book": text_book,
          "slider_val": slider_val
        }),
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          window.location = "/view_results";
        })
        .catch((error) => console.log(error));
  };