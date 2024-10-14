// document.addEventListener('DOMContentLoaded', function() {
//     const propertyTypeField = document.querySelector('[name="property_type"]');
//     const categoryField = document.querySelector('[name="category"]');
//     const subCategoryField = document.querySelector('[name="sub_category"]');

//     // Update categories when property type changes
//     propertyTypeField.addEventListener('change', function() {
//         const propertyType = this.value;
//         // Fetch categories based on property type
//         fetch(`/your_api/get-categories/?property_type=${propertyType}`)
//             .then(response => response.json())
//             .then(data => {
//                 // Populate category dropdown
//                 categoryField.innerHTML = '';
//                 data.categories.forEach(category => {
//                     const option = document.createElement('option');
//                     option.value = category.id;
//                     option.textContent = category.name;
//                     categoryField.appendChild(option);
//                 });
//                 // Clear sub-category dropdown
//                 subCategoryField.innerHTML = '';
//             });
//     });

//     // Update subcategories when category changes
//     categoryField.addEventListener('change', function() {
//         const categoryId = this.value;
//         // Fetch subcategories based on selected category
//         fetch(`/your_api/get-subcategories/?category_id=${categoryId}`)
//             .then(response => response.json())
//             .then(data => {
//                 // Populate sub-category dropdown
//                 subCategoryField.innerHTML = '';
//                 data.subcategories.forEach(subcategory => {
//                     const option = document.createElement('option');
//                     option.value = subcategory.id;
//                     option.textContent = subcategory.name;
//                     subCategoryField.appendChild(option);
//                 });
//             });
//     });
// });