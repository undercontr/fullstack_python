$(".carousel").carousel()

$('#myTab a').on('click', function (e) {
    e.preventDefault()
    $(this).tab('show')
})

$(document).on("keypress", 'form', function (e) {
    let code = e.keyCode || e.which;
    if (code === 13) {
        e.preventDefault();
        return false;
    }
});

let loadingSpinner = $("#loading-spinner")

loadingSpinner.hide()

let searchRequest = null;
let docRequest = null;
let searchBox = $("#searchbox");
let searchFieldBottomText = $("#search-field-bottom-text");
let searchResults = $("#search-results")
let quotationForm = $("#quotation-form")
let contactForm = $("#contact-form")
let docBox = $("#docbox")
let docResults = $("#docresults")

$(document).ready(function () {
    let minlength = 3;

    searchBox.keyup(function () {
        let that = this,
            value = $(this).val();

        if (value.length >= minlength) {
            if (searchRequest != null)
                searchRequest.abort();
            searchRequest = $.ajax({
                type: "POST",
                url: "/get_search_data",
                data: {
                    "searchbox": value,
                    "csrf_token": $("#csrf_token").val()
                },
                dataType: "json",
                success: function (data) {
                    //we need to check if the value is the same

                    console.log(data)

                    if (value === $(that).val()) {
                        if (searchBox.val() !== "") {

                            searchResults.removeClass("d-none")
                            searchBox.addClass("border-bottom-0")
                            searchResults.addClass("border-top-0")
                            searchFieldBottomText.addClass("visible")

                        }

                        searchResults.html("<p class='text-small badge badge-pill badge-secondary m-2'><span class='m-2'> Result for: " + value + "</span></p>")

                        if (Object.keys(data).length === 0) {
                            searchResults.append("<br><b class='m-2'>There is no result for this query</b>")
                        } else if (Object.keys(data).length > 7) {
                            searchResults.append("<a href='" + window.search_url + "?q=" + value + "&page=1" +"' class='text-small badge badge-pill badge-dark m-2'><span class='m-2'>Click here or press enter for all search results</span></a>")

                            searchBox.on('keypress', function(e) {
                                if (e.which === 13) {

                                    window.location.href =  window.search_url + "?q=" + value + "&page=1"

                                }
                            })
                        }



                        data.forEach(function (i) {
                            if (i.cas_number === null) {
                                i.cas_number = "Not Available";
                            }

                            let result = "    <div class=\"row  m-2 bg-light border\">\n" +
                                "        <div class=\"col m-2\">\n" +
                                "            <span class=\"font-weight-bold\"><a class='text-dark' href='" + window.product_url + i.url + "'>" + i.name + "</a></span><br>\n" +
                                "            <span class=\"badge badge-pill small badge-warning\">CAS: " + i.cas_number + "</span>&nbsp;\n" +
                                "            <span class=\"badge badge-pill small badge-secondary\">Model: " + i.model + "</span>&nbsp;\n" +
                                // "            <span class=\"badge badge-pill small badge-primary\">100ml</span>&nbsp;\n" +
                                // "            <span class=\"badge badge-pill small badge-primary\">1 LT</span>&nbsp;\n" +
                                // "            <span class=\"badge badge-pill small badge-primary\">5 LT</span>&nbsp;\n" +
                                "        </div>\n" +
                                "    </div>\n"
                            searchResults.append(result)
                        })

                        if (Object.keys(data).length === 1) {

                            searchBox.on('keypress', function (e) {
                                if (e.which === 13) {

                                    window.single_page = window.product_url + data[0].url

                                    window.location.href = window.single_page
                                }
                            });

                        }

                    }
                }
            });
        }
    });
    searchBox.keyup(function () {

        // If value is not empty
        if ($(this).val().length === 0) {
            // Hide the element by add d-none of Bootstrap
            searchResults.addClass("d-none")
            searchBox.removeClass("border-bottom-0")
            searchResults.removeClass("border-top-0")
            searchFieldBottomText.removeClass("visible")
            searchResults.html('')

        }
    }).keyup();

    searchBox.keyup(function (e) {
        if (e.keyCode === 27) {
            searchResults.addClass("d-none")
            searchBox.removeClass("border-bottom-0")
            searchResults.removeClass("border-top-0")
            searchFieldBottomText.removeClass("visible")
            searchResults.html('')
            searchBox.val("")
        }

    });
});

quotationForm.submit(function (e) {

    loadingSpinner.show()

    $.ajax({
        type: "POST",
        url: window.quotation_url,
        data: {
            "csrf_token": $("#csrf_token").val(),
            "name_surname": $("#name_surname").val(),
            "company": $("#company").val(),
            "country": $("#country").val(),
            "email": $("#email").val(),
            "phone": $("#phone").val(),
            "product_name": $("#product_name").val(),
            "product_sku": $("#product_sku").val(),
            "qty": $("#qty").val(),
            "message": $("#message").val(),
            "g-recaptcha-response": grecaptcha.getResponse()
        },
        dataType: "json",
        success: function (data) {
            $("#modal-title").append(data.name + ", your request is sent! <i\n" +
                "                            class=\"text-success fas fa-check-circle\"></i>")
            grecaptcha.reset()
            console.log(data)
        },
        complete: function () {
            loadingSpinner.hide()
            $("#mail-modal").modal("show")
        }

    })

    e.preventDefault()

})

contactForm.submit(function (e) {

    loadingSpinner.show()

    $.ajax({
        type: "POST",
        url: window.contact_url,
        data: {
            "csrf_token": $("#csrf_token").val(),
            "name_surname": $("#name_surname").val(),
            "company": $("#company").val(),
            "country": $("#country").val(),
            "email": $("#email").val(),
            "phone": $("#phone").val(),
            "message": $("#message").val(),
            "g-recaptcha-response": grecaptcha.getResponse()
        },
        dataType: "json",
        success: function (data) {
            $("#modal-title").append(data.name + ", your request is sent! <i\n" +
                "                            class=\"text-success fas fa-check-circle\"></i>")
            grecaptcha.reset()
            console.log(data)
        },
        complete: function () {
            loadingSpinner.hide()
            $("#mail-modal").modal("show")
        }

    })

    e.preventDefault()

})


$(document).ready(function () {
    let minlength = 6;

    docBox.keyup(function () {
        let that = this,
            value = $(this).val();

        if (value.length >= minlength) {
            if (docRequest != null)
                docRequest.abort();
            docRequest = $.ajax({
                type: "POST",
                url: "/get_docs_data",
                data: {
                    "docbox": value,
                    "csrf_token": $("#csrf_token").val()
                },
                dataType: "json",
                success: function (data) {
                    //we need to check if the value is the same

                    console.log(data)

                    if (value === $(that).val()) {
                        if (docBox.val() !== "") {


                        }

                        // docResults.html("<p class='badge badge-primary my-2'><span class='my-2'> Result for: " + value + "</span></p>")
                        if (Object.keys(data).length === 0) {
                            docResults.html("<br><b class='m-2'>There is no result for this query</b>")
                        } else if (Object.keys(data).length === 1) {
                            docResults.html("")
                        }


                        data.forEach(function (i) {

                            let result = "        <div class=\"list-group-item list-group-item-action flex-column align-items-start\">\n" +
                                "            <div class=\"row\">\n" +
                                "                <div class=\"col-md-12\">\n" +
                                "                    <div class=\"d-flex w-100 justify-content-between\"><h4 class=\"mb-1\">" + i.model + "</h4><h5>" + i.name + "</h5><small\n" +
                                "                            style=\"cursor:default\"><span\n" +
                                "                            class=\"font-weight-bold\"><a href=\"" + window.product_url + "/" + i.url + "\">Product Page</a></span></small>\n" +
                                "                    </div>\n" +
                                "                    <p class=\"my-3\" style=\"cursor:default\">\n" +
                                "\n" +
                                "                        <a href=\"" + window.static_url + "msds/" + i.msds + "\" class=\"btn btn-success btn-sm\">" + i.msds + "</a> <a href=\"" + window.static_url + "tds/" + i.tds + "\"\n" +
                                "                                                                                         class=\"btn btn-success btn-sm\">" + i.tds + "</a>\n" +
                                "\n" +
                                "                    </p>\n" +
                                "                </div>\n" +
                                "            </div>\n" +
                                "        </div>"
                            docResults.append(result)
                        })

                    }
                }
            });
        }
    });
    docBox.keyup(function () {

        // If value is not empty
        if ($(this).val().length === 0) {
            // Hide the element by add d-none of Bootstrap
            docResults.html('')

        }
    }).keyup();

    docBox.keyup(function (e) {
        if (e.keyCode === 27) {
            docResults.html("")
            docBox.val("")
        }

    });
});