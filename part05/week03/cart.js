function checkItem(item){
    let chk_id = item.id.split('-')[1];
    let chk_tr = document.getElementById('tr-' + chk_id);
    let goods_num = parseInt(document.getElementById('btnIpt-' + chk_id).value);
    chk_tr.style.backgroundColor = '';
    if (item.checked && goods_num > 0) {
        chk_tr.style.backgroundColor = "#f5e6cf";
    }else{
        item.checked = false;
    }
    let chk_price = document.getElementById('cart-price-' + chk_id);
    let cart_price = parseFloat(chk_price.textContent.slice(1));
    let sum_price = parseFloat(document.getElementById('sum-price').textContent.slice(1));
    if (item.checked) {
        sum_price += cart_price;
    } else {
        sum_price -= cart_price;
    }
    document.getElementById('sum-price').textContent = "￥" + sum_price.toFixed(2);
}

function checkAll(chk){
    let item_all = document.getElementsByName('chkItem');
    document.getElementById('sum-price').textContent = "￥0.00";
    document.getElementById('chk-all').checked = chk.checked;
    document.getElementById('chk-jd').checked = chk.checked;
    document.getElementById('chk-settlement').checked = chk.checked;
    for (let item of item_all){
        item.checked = chk.checked;
        if (item.checked){
           checkItem(item);
        }else{
            let chk_id = item.id.split('-')[1];
            let chk_tr = document.getElementById('tr-' + chk_id);
            chk_tr.style.backgroundColor = '';
        }
    }
}

function checkDelete(chkAll=false){
    let item_all = document.getElementsByName('chkItem');
    for(let i=item_all.length; i>0; i--){
        if(item_all[i-1].checked || chkAll){
            let chk_id = item_all[i-1].id.split('-')[1];
            let chk_tr = document.getElementById('tr-' + chk_id);
            console.log(chk_tr);
            chk_tr.remove();
        }
    }
    document.getElementById('chk-all').checked = false;
    document.getElementById('chk-jd').checked = false;
    document.getElementById('chk-settlement').checked = false;
    document.getElementById('sum-price').textContent = "￥0.00";
}

function numDelete(item){
    let btn_id = item.id.split('-')[1];
    let goods_num = parseInt(document.getElementById('btnIpt-' + btn_id).value);
    if(goods_num > 0){
        document.getElementById('btnIpt-' + btn_id).value = goods_num - 1;
        let goods_price = parseFloat(document.getElementById('cart-price-' + btn_id).dataset.price);
        let chk_price = parseFloat(document.getElementById('cart-price-' + btn_id).textContent.slice(1)) - goods_price;
        document.getElementById('cart-price-' + btn_id).textContent = '￥' + chk_price.toFixed(2);
        let chk_item = document.getElementById('chk-' + btn_id);
        chk_item.checked = true;
        numRefreshPrice(chk_item);
    }
}

function numAdd(item){
    let btn_id = item.id.split('-')[1];
    let goods_num = parseInt(document.getElementById('btnIpt-' + btn_id).value);
    document.getElementById('btnIpt-' + btn_id).value = goods_num + 1;
    let goods_price = parseFloat(document.getElementById('cart-price-' + btn_id).dataset.price);
    let chk_price = parseFloat(document.getElementById('cart-price-' + btn_id).textContent.slice(1)) + goods_price;
    document.getElementById('cart-price-' + btn_id).textContent = '￥' + chk_price.toFixed(2);
    let chk_item = document.getElementById('chk-' + btn_id);
    chk_item.checked = true;
    numRefreshPrice(chk_item);
}

function numRefreshPrice(item){
    let chk_id = item.id.split('-')[1];
    let item_all = document.getElementsByName('chkItem');
    document.getElementById('sum-price').textContent = "￥0.00";
    for (let item of item_all){
        if (item.checked){
           checkItem(item);
        }
    }
}

function settlement(){
    let settlement_price = document.getElementById('sum-price').textContent;
    alert("总价："+settlement_price);
}
