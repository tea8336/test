$(
    checkItem(), checkAll(), checkDelete(), cartClear(), numDelete(), numAdd(), settlement()
)

function checkItem() {
    $('input[name="chkItem"]').on('click', function() {
        let item_id = $(this).prop('id').split('-')[1];
        let chk_tr = $('#tr-' + item_id);
        chk_tr.css('backgroundColor', '');
        if($(this).prop('checked')) {
            chk_tr.css('backgroundColor', '#f5e6cf');
        }else{
            $(this).prop('checked', false);
            $('#chk-all').prop('checked', false);
            $('#chk-jd').prop('checked', false);
            $('#chk-settlement').prop('checked', false);
        }
        let chk_price = $('#cart-price-' + item_id);
        let cart_price = parseFloat(chk_price.prop('textContent').slice(1));
        let sum_price = parseFloat($('#sum-price').prop('textContent').slice(1));
        if($(this).prop('checked')) {
            sum_price += cart_price;
        }else{
            sum_price -= cart_price;
        }
        $('#sum-price').text('￥' + sum_price.toFixed(2));
    })
}

function checkAll() {
    $('input[name="chkAll"]').on('click', function() {
        let chkAll_chk = $(this).prop('checked');
        let item_all = $('input[name="chkItem"]');
        $('#sum-price').text('￥0.00');
        $('#chk-all').prop('checked', chkAll_chk);
        $('#chk-jd').prop('checked', chkAll_chk);
        $('#chk-settlement').prop('checked', chkAll_chk);
        if(chkAll_chk) {
            let sum_price = 0;
            item_all.each(function(){
                let item = $(this);
                item.prop('checked', true);
                item.parent().parent().css('backgroundColor', '#f5e6cf');
                sum_price += parseFloat(item.parent().siblings().find('p[name="cartPrice"]').prop('textContent').slice(1));
            })
            $('#sum-price').text('￥' + sum_price.toFixed(2));
        }else{
            item_all.each(function(){
                let item = $(this);
                item.prop('checked', false);
                item.parent().parent().css('backgroundColor', '');
                $('#sum-price').text('￥0.00');
            })
        }
    })
}

function checkDelete() {
    $('a[name="chkDelete"]').on('click', function() {
        let tr_all = $('tr[name="cartTr"]');
        tr_all.each(function(){
            let item = $(this);
            if(item.find('input[name="chkItem"]').prop('checked')) {
                item.remove();
            }
        })
        numRefreshPrice(); 
    })
}

function cartClear() {
    $('a[name="cartClear"]').on('click', function() {
        $('tr[name="cartTr"]').remove();
        numRefreshPrice(); 
    })
}

function numDelete() {
    $('input[name="goodsNumDel"]').on('click', function() {
        let item_id = $(this).prop('id').split('-')[1];
        let goods_num = parseInt($('#btnIpt-' + item_id).prop('value'));
        if(goods_num > 1) {
            let item_tr = $('#btnIpt-' + item_id).parent().parent();
            item_tr.find('input[name="chkItem"]').prop('checked', true);
            item_tr.css('backgroundColor', '#f5e6cf');
            item_tr.find('input[name="goodsNumInput"]').prop('value', goods_num - 1);
            let unit_price = parseFloat(item_tr.find('p[name="cartPrice"]').prop('dataset').price);
            let goods_price = parseFloat(item_tr.find('p[name="cartPrice"]').prop('textContent').slice(1)) - unit_price;
            item_tr.find('p[name="cartPrice"]').text('￥' + goods_price.toFixed(2));
            numRefreshPrice(); 
        }
    })
}

function numAdd() {
    $('input[name="goodsNumAdd"]').on('click', function() {
        let item_id = $(this).prop('id').split('-')[1];
        let item_tr = $('#btnIpt-' + item_id).parent().parent();
        item_tr.find('input[name="chkItem"]').prop('checked', true);
        item_tr.css('backgroundColor', '#f5e6cf');
        let goods_num = parseInt($('#btnIpt-' + item_id).prop('value'));
        item_tr.find('input[name="goodsNumInput"]').prop('value', goods_num + 1);
        let unit_price = parseFloat(item_tr.find('p[name="cartPrice"]').prop('dataset').price);
        let goods_price = parseFloat(item_tr.find('p[name="cartPrice"]').prop('textContent').slice(1)) + unit_price;
        item_tr.find('p[name="cartPrice"]').text('￥' + goods_price.toFixed(2));
        numRefreshPrice();    
    })
}

function numRefreshPrice() {
    let item_all = $('input[name="chkItem"]');
    let sum_price = 0;
    item_all.each(function(){
        let item = $(this);
        if(item.prop('checked')) {
            sum_price += parseFloat(item.parent().parent().find('p[name="cartPrice"]').prop('textContent').slice(1));
        }
    })
    $('#sum-price').text('￥' + sum_price.toFixed(2));
}

function settlement() {
    $('input[name="settlement"]').on('click', function() {
        let settlement_price = $('#sum-price').prop('textContent');
        alert("总价："+settlement_price);
    })
}
