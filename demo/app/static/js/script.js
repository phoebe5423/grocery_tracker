$(document).ready(function () {
    $('#item-modal').on('show.bs.modal', function (event) {

    });

    $('#submit-new-prod').click(function(){
        $('#form-new-prod').submit();
    });
});

// $(document).ready(function () {
    $('#modal-edit-product').on('show.bs.modal', function (event) {

    })

    $('#submit-edit-prod').click(function(){
        $('#form-edit-prod').submit();
    });
// });

    $('#modal-add-toinv').on('show.bs.modal', function (event) {

        })

        $('#submit-add-toinv').click(function(){
            $('#form-edit-prod').submit();
        });


$(document).ready(function(){
    var date_input=$('input[name="date"]'); //our date input has the name "date"
    var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
    date_input.datepicker({
        format: 'yyyy/mm/dd',
        container: container,
        todayHighlight: true,
        autoclose: true,
    })
})


// $(document).ready(function () {
    $('#store-modal').on('show.bs.modal', function (event) {

    });

    $('#submit-new-store').click(function(){
        $('#form-new-store').submit();
    });
// });

// $(document).ready(function () {
    $('#modal-edit-store').on('show.bs.modal', function (event) {

    })

    $('#submit-edit-store').click(function(){
        $('#form-edit-store').submit();
    });
// });