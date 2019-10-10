let productContainer = document.getElementById('product-container');
let container = document.getElementById('container');
if (productContainer) {
    let currentRow = null
    let products = productContainer.children;
    let numProducts = products.length

    // Display only 3 products per row
    if (numProducts > 3) {
        for (let index = 0; index < numProducts; index++) {
            if (index % 3 == 0) {
                currentRow = document.createElement('DIV');
                currentRow.className += 'row';
                container.appendChild(currentRow);
            }

            // Limit length of text in description on home page
            let productDescription = products[0].getElementsByClassName('col-md-4')[0].getElementsByTagName('p')[0];
            if (productDescription.innerHTML.length > 100) {
                productDescription.innerHTML = productDescription.innerHTML.slice(0, 100) + '...';
            }

            currentRow.appendChild(products[0]);
        }
    }
}