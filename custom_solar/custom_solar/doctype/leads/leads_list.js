frappe.listview_settings["Leads"] = {
    onload: function (listview) {
        listview.page.fields_dict['name'].$wrapper.attr('data-original-title', __('Search Lead'))
            .find('input').attr('placeholder', __('Search Lead'));

        listview.get_args = function () {  
            let args = frappe.views.ListView.prototype.get_args.call(listview);  
            console.log("args", args);
            args.filters.some((f, i) => {
                if (f[1] === 'name') { 
                    return args.or_filters = [
                        args.filters.splice(i, 1)[0],  
                        [f[0], 'name', f[2], f[3]],
                        [f[0], 'full_name', f[2], f[3]],
                    ];
                }
            });

            return args;
        }
    },
    refresh: function (listview) {
        $("span.list-liked-by-me, .list-count, .list-row-like, .modified, .level-right").hide();
    },
};

frappe.listview_settings['Leads'] = {  
    button: {
        show: function(doc) {
            return doc.status !== 'closed'; 
        },
        get_label: function() {
            return __('Create Site Visit');
        },
        get_description: function(doc) {
            return __("Create a Site Visit for Lead: {0}", [doc.full_name]);
        },
        action: function(doc) {
            create_site_visit_for_lead(doc);
        }
    }
};


function create_site_visit_for_lead(doc) {

    frappe.ui.form.on('Site_Visit', {
        onload: function(frm) {
            frm.set_value('lead_owner', frappe.session.user);
            frm.set_value('lead', doc.name);  
        }
    });
    frappe.set_route('Form', 'Site_Visit', 'new');
}






