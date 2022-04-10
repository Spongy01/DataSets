let attributes=0


// fixed, dont change, caution
function removeAttribute(id){
    // alert("Received ID : "+id)
    const child = document.getElementById('attribute_'+id);
    child.parentNode.removeChild(child)
    // alert("Current Arrtibutes : "+attributes)
    let iden = parseInt(id)
    for (let i= iden+1 ; i <= attributes; i++){


        // alert("Updating Other Indices, current i : "+i)
        div = document.getElementById('attribute_'+i)
        div.setAttribute('id','attribute_'+(i-1))

        input = document.getElementById('column_name_'+i)
        input.setAttribute('id','column_name_'+(i-1))
        // input.setAttribute('value','Attribute : '+(i-1))
        input.setAttribute('name','column_name_'+(i-1))

        input = document.getElementById('column_size_'+i)
        input.setAttribute('id','column_size_'+(i-1))
        input.setAttribute('name','column_size_'+(i-1))

        input = document.getElementById('column_size_d_'+i)
        input.setAttribute('id','column_size_d_'+(i-1))
        input.setAttribute('name','column_size_d_'+(i-1))

        input = document.getElementById('datatype_'+i)
        input.setAttribute('id','datatype_'+(i-1))
        input.setAttribute('name','datatype_'+(i-1))

       // alert("Updating Other Indices 2, current i : "+i)


        input = document.getElementById('unique_check_'+i)
        input.setAttribute('id','unique_check_'+(i-1))
        input.setAttribute('name','unique_check_'+(i-1))
        input = document.getElementById('unique_label_'+i)
        input.setAttribute('for','unique_label_'+(i-1))
        input.setAttribute('id','unique_label_'+(i-1))

        //alert("Updating Other Indices 2.1, current i : "+i)

        input = document.getElementById('blank_check_'+i)
        input.setAttribute('id','blank_check_'+(i-1))
        input.setAttribute('name','blank_check_'+(i-1))

        // alert("Updating Other Indices 2.1.1, current i : "+i)

        input = document.getElementById('blank_label_'+i)

       // alert("Updating Other Indices 2.1.2, current i : "+i)

        input.setAttribute('for','blank_check_'+(i-1))

       // alert("Updating Other Indices 2.1.3, current i : "+i)

        input.setAttribute('id','blank_label_'+(i-1))



        input = document.getElementById(i)
        input.setAttribute('id',(i-1))
        // input.removeEventListener('click', function (){
        //
        //     removeAttribute(i)
        // });
        //
        //
        //
        // input.addEventListener('click', function (){
        //
        //     removeAttribute((i-1))
        // });
        // alert("Updated index current i : "+i)
    }

    attributes=attributes-1
    //alert("Now attributes are : "+attributes)
    document.getElementById('no_of_attributes').value =parseInt(attributes)

}


// fixed, dont change caution
function addAttribute(){
    attributes+=1
    document.getElementById('no_of_attributes').value =parseInt(attributes)
    let div = document.createElement('div')
    div.setAttribute("class","card mt-3")
    div.setAttribute("id","attribute_"+attributes)
    document.getElementById('attributes').appendChild(div)

    let div_body = document.createElement('div')
    div_body.setAttribute("class","card-body p-2")
    div.appendChild(div_body)

    let row1 = document.createElement('div')
    row1.setAttribute("class","mb-1 row p-2")
    div_body.appendChild(row1)

    let col1 = document.createElement('div')
    col1.setAttribute("class","col-8")
    row1.appendChild(col1)

    let input1 = document.createElement('input')
    input1.setAttribute("type", "text")
    // input1.setAttribute("value", "Attribute : "+attributes)
    input1.setAttribute("class", "form-control")
    input1.required = true
    input1.setAttribute("name", "column_name_"+attributes)
    input1.setAttribute("id", "column_name_"+attributes)
    input1.setAttribute("placeholder", "Column Name ( Spaces( ) will be converted to underscores(_) )")
    col1.appendChild(input1)


    let col3 =document.createElement('div')
    col3.setAttribute("class","col-4")
    row1.appendChild(col3)

    let input3 = document.createElement('select')
    input3.setAttribute("class", "form-select")
    input3.setAttribute("name", "datatype_"+attributes)
    input3.setAttribute("id", "datatype_"+attributes)
    input3.onchange = function () {
        index = input3.id.search('_')
        let my_id = parseInt(input3.id.slice(index+1))
        if (input3.value ==='Number-float'){

            document.getElementById("column_size_d_"+my_id).disabled = false
        }
        else{

            document.getElementById("column_size_d_"+my_id).disabled = true
        }
    }
    col3.appendChild(input3)

    let option = document.createElement('option')

    // option.innerHTML="Choose DataType"
    // input3.appendChild(option)

    option = document.createElement('option')
    option.setAttribute("value","Text")
    option.setAttribute("selected","")
    option.innerHTML="Text"
    input3.appendChild(option)

    option = document.createElement('option')
    option.setAttribute("value","Number")
    option.innerHTML="Number(wihout decimal)"
    input3.appendChild(option)

    option = document.createElement('option')
    option.setAttribute("value","Number-float")
    option.innerHTML="Number(wih decimal)"
    input3.appendChild(option)

    option = document.createElement('option')
    option.setAttribute("value","Date")
    option.innerHTML="Date"
    input3.appendChild(option)

    option = document.createElement('option')
    option.setAttribute("value","Date/Time")
    option.innerHTML="Date/Time"
    input3.appendChild(option)

    option = document.createElement('option')
    option.setAttribute("value","blob")
    option.innerHTML="Random"
    input3.appendChild(option)

    let col2 = document.createElement('div')
    col2.setAttribute("class","col-3 pt-2")
    row1.appendChild(col2)

    let input2 = document.createElement('input')
    input2.setAttribute("type", "number")
    input2.setAttribute("class", "form-control")
    input2.setAttribute("name", "column_size_"+attributes)
    input2.setAttribute("id", "column_size_"+attributes)
    input2.setAttribute("placeholder", "Data Size (Characters)")
    col2.appendChild(input2)

    let col4 = document.createElement('div')
    col4.setAttribute("class","col-3 pt-2")
    row1.appendChild(col4)

    let input4 = document.createElement('input')
    input4.setAttribute("type", "number")
    input4.setAttribute("class", "form-control")
    input4.setAttribute("name", "column_size_d_"+attributes)
    input4.setAttribute("id", "column_size_d_"+attributes)
    input4.setAttribute("disabled","")
    input4.setAttribute("placeholder", "Decimals(Numbers)")
    col4.appendChild(input4)

    let row2 = document.createElement("div")
    row2.setAttribute("class","mb-1 p-2 d-flex justify-content-between align-items-center")
    div_body.appendChild(row2)

    let grp = document.createElement("div")
    row2.appendChild(grp)

    let unqval = document.createElement("div")
    unqval.setAttribute("class","form-check form-check-inline")
    grp.appendChild(unqval)

    let unqinp = document.createElement("input")
    unqinp.setAttribute("class","form-check-input")
    unqinp.setAttribute("type","checkbox")
    unqinp.setAttribute("value","1")
    unqinp.setAttribute("name","unique_check_"+attributes)
    unqinp.setAttribute("id","unique_check_"+attributes)
    unqval.appendChild(unqinp)

    let unqlbl = document.createElement("label")
    unqlbl.setAttribute("class","form-check-label")
    unqlbl.setAttribute("id","unique_label_"+attributes)
    unqlbl.setAttribute("for","unique_check_"+attributes)
    unqlbl.innerHTML="Unique Values"
    unqval.appendChild(unqlbl)

    let blnkval = document.createElement("div")
    blnkval.setAttribute("class","form-check form-check-inline")
    grp.appendChild(blnkval)

    let blnkinp = document.createElement("input")
    blnkinp.setAttribute("class","form-check-input")
    blnkinp.setAttribute("type","checkbox")
    blnkinp.setAttribute("value","2")
    blnkinp.setAttribute("name","blank_check_"+attributes)
    blnkinp.setAttribute("id","blank_check_"+attributes)
    blnkval.appendChild(blnkinp)

    let blnklbl = document.createElement("label")
    blnklbl.setAttribute("class","form-check-label")
    blnklbl.setAttribute("id","blank_label_"+attributes)
    blnklbl.setAttribute("for","blank_check_"+attributes)
    blnklbl.innerHTML="Can Be Blank"
    blnkval.appendChild(blnklbl)

    grp = document.createElement("div")
    row2.appendChild(grp)

    let del = document.createElement("button")
    del.setAttribute("type","button")
    del.setAttribute("class","btn btn-danger")
    del.setAttribute("id",attributes)

    del.addEventListener('click',function (){
        removeAttribute(del.id)
    });

    // del.setAttribute('onClick',"removeAttribute("+(attributes)+")");
    del.innerHTML="Delete";

    grp.appendChild(del);
}

// document.getElementById('myButton').addEventListener('click',function(){
//     //do something
// });
