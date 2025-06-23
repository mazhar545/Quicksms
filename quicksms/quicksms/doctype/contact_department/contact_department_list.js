frappe.listview_settings['Contact Department'] = {
    onload: function(listview) {
        listview.page.add_button(__('Fetch Departments'), function() {
            // Show message that we are fetching department names
            frappe.msgprint(__('Fetching department count... Please wait.'));
            
            // Fetch the count of departments
            frappe.call({
                method: 'frappe.client.get_count',
                args: {
                    doctype: 'Department'  // Fetch the department count from the Department doctype
                },
                callback: function(response) {
                    if (response.message) {
                        const departmentCount = response.message;
                        // Show department count in a message
                        frappe.msgprint(__('Total departments in the system: ') + departmentCount);

                        // Now proceed to fetch the actual department names
                        let allDepartments = [];
                        let page = 0;
                        let limit = 100;  // Set the page size for fetching records

                        // Function to fetch departments in chunks
                        function fetchDepartments() {
                            frappe.call({
                                method: 'frappe.client.get_list',
                                args: {
                                    doctype: 'Department',   // Fetch from the Department doctype
                                    fields: ['department_name'],  // Fetch only the department_name field
                                    limit_page_length: limit,    // Set the page size for fetching records
                                    start: page * limit        // Set the starting point for pagination
                                },
                                callback: function(response) {
                                    console.log(response.message);  // Check what data is being returned

                                    if (response.message && response.message.length > 0) {
                                        allDepartments = allDepartments.concat(response.message); // Add fetched departments
                                        page++;  // Increment the page number

                                        // If the number of records fetched is equal to the page size, keep fetching
                                        if (response.message.length === limit) {
                                            fetchDepartments();  // Continue fetching next page
                                        } else {
                                            // All departments fetched, now save them
                                            saveDepartments(allDepartments);
                                        }
                                    } else {
                                        frappe.msgprint(__('No departments found.'));
                                    }
                                },
                                error: function(err) {
                                    // Handle errors in fetching departments
                                    console.error('Error fetching departments:', err);
                                    frappe.msgprint(__('Error fetching departments: ') + err.message);
                                }
                            });
                        }

                        // Function to save the fetched departments into 'Contact Department'
                        function saveDepartments(departments) {
                            departments.forEach(function(department) {
                                console.log("Fetched Department:", department.department_name);  // Log each department name

                                // Normalize department name: trim whitespace but keep it exact
                                let departmentName = department.department_name.trim();

                                // Check if department already exists in 'Contact Department'
                                frappe.call({
                                    method: 'frappe.client.get_list',
                                    args: {
                                        doctype: 'Contact Department',  
                                        filters: { 'department_name': departmentName },  // Filter by department_name
                                        fields: ['name']  // Only fetch the 'name' field
                                    },
                                    callback: function(existingDepartments) {
                                        if (existingDepartments.message.length === 0) {
                                            // If no department found, save it
                                            frappe.call({
                                                method: 'frappe.client.insert',
                                                args: {
                                                    doc: {
                                                        doctype: 'Contact Department',
                                                        department_name: departmentName
                                                    }
                                                },
                                                callback: function(insert_response) {
                                                    if (insert_response.message) {
                                                        console.log('Department saved:', department.department_name);  // Log successful save
                                                        frappe.msgprint(__('Department name: ') + department.department_name + __(' saved successfully.'));
                                                    } else {
                                                        console.error('Error saving department:', department.department_name);
                                                        frappe.msgprint(__('Error saving department: ') + department.department_name);
                                                    }
                                                }
                                            });
                                        } else {
                                            console.log('Department already exists:', department.department_name);  // Log duplicate
                                        }
                                    }
                                });
                            });
                            frappe.msgprint(__('Departments fetched and saved successfully.'));
                        }

                        fetchDepartments(); // Start fetching the data
                    } else {
                        frappe.msgprint(__('Error fetching department count.'));
                    }
                },
                error: function(err) {
                    // Handle errors in fetching department count
                    console.error('Error fetching department count:', err);
                    frappe.msgprint(__('Error fetching department count: ') + err.message);
                }
            });
        });
    }
};
