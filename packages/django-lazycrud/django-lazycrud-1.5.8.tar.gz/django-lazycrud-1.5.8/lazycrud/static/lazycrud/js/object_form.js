function lazycrud_form_init(form_id) {
    var datetimepicker_icons = {
        time: "fa fa-clock-o",
        date: "fa fa-calendar",
        previous: "fa fa-chevron-left",
        next: "fa fa-chevron-right",
        up: "fa fa-chevron-circle-up",
        down: "fa fa-chevron-circle-down",
        close: "fa fa-times",
    };

    $(form_id + ' .dateinput').datetimepicker({
        format: 'DD/MM/YYYY',
        icons: datetimepicker_icons,
    });

    $(form_id + ' .timeinput').datetimepicker({
        format: 'HH:mm',
        icons: datetimepicker_icons,
        stepping: 15,
    });

    $(form_id + ' .datetimeinput').datetimepicker({
        locale: 'it',
        icons: datetimepicker_icons,
        stepping: 15,
        showClose: true,
    });
}

$(function() {
    lazycrud_form_init('form');
});
