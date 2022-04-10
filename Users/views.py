from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.db import connection, IntegrityError, transaction

from .forms import LoginForm, RegisterForm, CreateFolderForm, CreateTableForm

# Create your views here.
from .models import CustomUser, FolFolRel, FolTabRel


def landing_view(request):
    return render(request, 'Users/landing.html')


def login_view(request):
    if request.method == "GET":
        return render(request, 'Users/login.html')
    else:
        loginForm = LoginForm(request.POST, request.FILES)
        if loginForm.is_valid():
            email = loginForm.cleaned_data['email']
            password = loginForm.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                # Valid User
                username = user.username
                login(request, user)
                return redirect(home_view)
            else:
                return HttpResponse("Not a Valid User")

        return HttpResponse("Invalid Values")


def register_view(request):
    if request.method == 'GET':
        return render(request, 'Users/register.html', {
            'message': "",
            "Present": False
        })
    else:
        registerForm = RegisterForm(request.POST, request.FILES)
        if registerForm.is_valid():
            email = registerForm.cleaned_data['email']
            pass1 = registerForm.cleaned_data['password1']
            pass2 = registerForm.cleaned_data['password2']
            username = registerForm.cleaned_data['username']

            if pass1 == pass2:
                #  user valid
                try:
                    user = CustomUser.objects.create_user(email=email, password=pass1, username=username)
                    login(request, user)
                    return redirect(home_view)
                except IntegrityError:
                    return render(request, 'Users/register.html', {
                        'message': "",
                        "Present": True

                    })
            else:
                return render(request, 'Users/register.html', {
                    'message': "Passwords Do not Match",
                    "Present": False
                })
        else:
            return render(request, 'Users/register.html', {
                'message': "Invalid Form Data",
                "Present": False
            })


def home_view(request):
    folder = 'Home'

    return redirect(folder_view, folder)
    # data = FolFolRel.objects.filter(p_folder=folder, user=request.user)
    # table_data_raw = FolTabRel.objects.filter(p_folder=folder, user=request.user, is_archived=False)
    # table_data = []
    #
    # for item in table_data_raw:
    #     table_data.append(item.get_c_table())
    #
    # tuplist = []
    # for item in data:
    #     tuplist.append(item.get_c_folder())
    #
    # url = ''
    # folderlist = folder.split('-')
    # urllist = []
    # url = url + folderlist[0]
    # tup = ()
    # for item in folderlist:
    #     if item == url:
    #         tup = (item, url)
    #     else:
    #         url = url + '-' + item
    #         tup = (item, url)
    #         print(tup)
    #     urllist.append(tup)
    #
    # print(urllist)
    # current = urllist[len(urllist) - 1]
    # return render(request, 'Users/home.html', {
    #     'data': tuplist,
    #     'folder': folder,
    #     'urllist': urllist,
    #     'current': current,
    #     'table_data': table_data,
    #     'User': request.user.username
    # })


@login_required
def logout_view(request):
    logout(request)
    return redirect(landing_view)


@login_required()
def create_folder_view(request):
    if request.method == 'POST':
        folder = CreateFolderForm(request.POST, request.FILES)
        if folder.is_valid():
            foldername = folder.cleaned_data['foldername']
            folderbrief = folder.cleaned_data['folderbrief']
            pfolder = folder.cleaned_data['pathto']

            present_data = FolFolRel.objects.filter(p_folder=pfolder, c_folder=foldername, c_folder_brief=folderbrief,
                                                    user=request.user)
            if len(present_data) == 0:
                fol = FolFolRel(p_folder=pfolder, c_folder=foldername, c_folder_brief=folderbrief, user=request.user)
                fol.save()
                return redirect(folder_view, folder=pfolder)

            else:
                # data exists
                return HttpResponse("Table with such id already exists in directory")
        else:
            return HttpResponse("Invalid Folder")

    else:
        return redirect(home_view)


@login_required()
def folder_view(request, folder):
    data = FolFolRel.objects.filter(p_folder=folder, user=request.user)
    table_data_raw = FolTabRel.objects.filter(p_folder=folder, user=request.user, is_archived=False)
    table_data = []
    tuplist = []

    for item in data:
        tuplist.append(item.get_c_folder())

    for item in table_data_raw:
        table_data.append(item.get_c_table())

    if request.method == 'POST':
        search_query = request.POST['seachBar']

        if search_query != '':
            tuplist = []
            table_data = []
            for item in data:
                if search_query in item.get_c_folder()[0]:
                    tuplist.append(item.get_c_folder())

            for item in table_data_raw:
                if search_query in item.get_c_table()[0]:
                    table_data.append(item.get_c_table())

    url = ''
    folderlist = folder.split('-')
    urllist = []
    url = url + folderlist[0]
    tup = ()
    for item in folderlist:
        if item == url:
            tup = (item, url)
        else:
            url = url + '-' + item
            tup = (item, url)
            print(tup)
        urllist.append(tup)

    print(urllist)
    current = urllist[len(urllist) - 1]
    return render(request, 'Users/home.html', {
        'data': tuplist,
        'folder': folder,
        'urllist': urllist,
        'current': current,
        'table_data': table_data,
        'User': request.user.username,
        'is_archived': False,
        'is_dashboard': True,
        'is_favourite': False,
    })


@login_required
def create_set_view(request, folder):
    if request.method == 'GET':
        return render(request, 'Users/new_set.html', {
            'current': folder
        })
    else:
        # Method post, data extraction
        # username
        username = request.user.username
        folderpath = folder.replace('-', '$')
        folderpath = folderpath.replace(' ', '_').replace("'", '_')
        tablename = request.POST["tablename"]
        tablebrief = request.POST["tablebrief"]
        # final Table name
        table_name = username + "$$" + folderpath + "$$" + tablename
        # print(table_name)
        # No of Columns
        no_of_attrs = request.POST['no_of_attributes']
        # print("no of attributes : ", no_of_attrs)

        # querycreation
        query = "create table {} (\nPrimKey Integer Primary Key Autoincrement,\n".format(table_name)
        for i in range(1, int(no_of_attrs) + 1):
            column_name = request.POST['column_name_{}'.format(i)]
            query += column_name + " "
            data_type = request.POST['datatype_{}'.format(i)]

            if data_type == "Text":
                query += "TEXT"
            elif data_type == "Number":
                query += "INTEGER"
            elif data_type == "Number-float":
                query += "REAL"
            elif data_type == "Date":
                query += "TEXT"
            elif data_type == "Date/Time":
                query += "TEXT"
            elif data_type == "blob":
                query += "TEXT"

            is_size = False

            try:
                column_size = request.POST['column_size_{}'.format(i)]
                print("column_size is  ", column_size)
                if column_size != '':
                    query += "({}".format(column_size)
                    is_size = True
            except KeyError:
                column_size = 0

            column_size_d = 0
            if data_type == 'Number-float':
                column_size_d = request.POST['column_size_d_{}'.format(i)]
                if column_size_d != '':
                    query += ",{}".format(column_size_d)

            if (is_size):
                query += ")"
            query += " "
            # if is_unique:
            try:
                is_unique = request.POST['unique_check_{}'.format(i)]
                print("It is Unique")
                query += "Unique "
            except KeyError:
                print("Not Unique")

            # if is_blank:
            try:
                is_blank = request.POST['blank_check_{}'.format(i)]
                print("blnak for {} is {} ".format(i, is_blank))
            except KeyError:
                print("Not Blank")
                query += "Not Null "
            # print(column_name, column_size, column_size_d, data_type)

            # no comma at last line, is syntax error
            if i != int(no_of_attrs):
                query += ",\n"

        query += ");"

        # final query is ready now for table creation.
        # table needs to be added to FolTabRel still yet pending
        print("Query is \n", query)

        # tablename table breife folder
        is_data = FolTabRel.objects.filter(p_folder=folder, c_table=tablename, c_table_brief=tablebrief,
                                           user=request.user)

        if len(is_data) == 0:
            # then can add this table
            with connection.cursor() as cursor:
                cursor.execute(query)

            tab = FolTabRel(p_folder=folder, c_table=tablename, c_table_brief=tablebrief, user=request.user)
            tab.save()

            return redirect(folder_view, folder=folder)

        return HttpResponse("Could not create Table")
        # return HttpResponse("Wait Buddy")


@login_required()
def view_set_view(request, folder, table, table_brief):
    # print(table_brief)
    is_table = FolTabRel.objects.filter(p_folder=folder, c_table=table, c_table_brief=table_brief, user=request.user,
                                        is_archived=False)
    print("Is table Check Before: ", is_table)
    if len(is_table) == 0:
        return HttpResponse("Table Does not exists, Table Brief is : {}".format(table_brief))
    fol = folder
    folder = folder.replace('-', '$').replace(' ', '_').replace("'", '_')
    tablename = request.user.username + "$$" + folder + "$$" + table
    table_meta = is_table[0].get_c_table()
    is_fav = is_table[0].is_table_fav()
    is_pinned = is_table[0].is_table_pinned()
    with connection.cursor() as cursor:
        cursor.execute("Pragma table_info({})".format(tablename))
        meta_data = cursor.fetchall()

    columndata = ""
    for coldta in meta_data:
        columndata += coldta[1] + "$"

    columndata = columndata[:-1]

    if request.method == 'GET':

        with connection.cursor() as cursor:
            cursor.execute("Select * from {};".format(tablename))
            row = cursor.fetchall()

        data = row
        no_of_items = len(data)
        indexing = range(1, len(data) + 1)
        mod = []

        for item in data:
            # print(item)
            ls = []
            for element, meta in zip(item, meta_data):
                # print(element, meta[1], meta[2])

                tup = (str(element), meta[1], meta[2])
                ls.append(tup)
            mod.append(ls)

        data = zip(indexing, mod)
        return render(request, 'Users/view_set.html', {
            'table_meta': table_meta,
            'is_fav': is_fav,
            'is_pinned': is_pinned,
            'data': data,
            'meta_data': meta_data,
            'folder': fol,
            'column_data': columndata,
            'items_count': no_of_items,
            'table': table,
            'table_brief': table_brief,
        })
    else:
        if 'query-submit' in request.POST:
            user_query = request.POST['querybox']
            start = 0
            end = len(user_query)
            query_builder = "Select "
            cols_to_show = '*'
            columndata = ""
            is_show = user_query.find('SHOW:', start, end)
            if is_show != -1:
                qnd = int(user_query.find(';', start, end))
                print("qnd is ", qnd)
                cols_to_show = user_query[start + 5: qnd]
                cols_to_show = 'PrimKey,' + cols_to_show
                cols_to_show_sep = cols_to_show.split(',')

                # columndata += 'PrimKey$'
                for coldta in meta_data:
                    if coldta[1] in cols_to_show_sep:
                        columndata += coldta[1] + "$"
                start = qnd + 1

                temp_meta = []
                for md in meta_data:
                    # if md[1] == 'PrimKey':
                    #     temp_meta.append(md)
                    if md[1] in cols_to_show_sep:
                        temp_meta.append(md)

                meta_data = temp_meta
                # print("meta is : ",meta_data)


            else:
                for coldta in meta_data:
                    columndata += coldta[1] + "$"
            columndata = columndata[:-1]

            query_builder += cols_to_show + " from " + tablename + "\n"
            is_where = user_query.find("WHERE:")
            if is_where != -1:
                qnd = user_query.find(';', start, end)
                where_query = user_query[start + 6: qnd]
                # where_query = where_query.split(',')
                start = qnd + 1
                query_builder += "where " + where_query + "\n"

            is_order_asc = user_query.find('ORDERBY-ASC:')
            if is_order_asc != -1:
                qnd = user_query.find(';', start, end)
                order_asc = user_query[start + 12: qnd]
                # order_asc = order_asc.split(',')
                start = qnd + 1
                query_builder += "order by " + order_asc + "\n"
            is_order_desc = user_query.find('ORDERBY-DESC:')
            if is_order_desc != -1:
                qnd = user_query.find(';', start, end)
                order_desc = user_query[start + 13: qnd]
                start = qnd + 1
                query_builder += "order by " + order_desc + " desc\n"

            query_builder += ';'
            print("Query is : ", query_builder)
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query_builder)
                    row = cursor.fetchall()

                data = row

                no_of_items = len(data)
                indexing = range(1, len(data) + 1)
                mod = []

                for item in data:

                    ls = []
                    for element, meta in zip(item, meta_data):
                        print(element, meta[1], meta[2])

                        tup = (str(element), meta[1], meta[2])
                        ls.append(tup)

                    mod.append(ls)
                data = zip(indexing, mod)
                return render(request, 'Users/view_set.html', {
                    'table_meta': table_meta,
                    'is_fav': is_fav,
                    'is_pinned': is_pinned,
                    'data': data,
                    'meta_data': meta_data,
                    'folder': fol,
                    'column_data': columndata,
                    'items_count': no_of_items,
                    'table': table,
                    'table_brief': table_brief,
                })

            except:
                return redirect(view_set_view, fol, table)

        if 'submit-edit-delete' in request.POST:
            id_edit = request.POST['edit_id']
            id_delete = request.POST['delete_id']
            id_edit = id_edit.split(',')
            id_delete = id_delete.split(',')
            columndata = request.POST['columndata']
            column_data = columndata.split('$')
            no_of_items = int(request.POST['itemscount'])
            is_fav = request.POST['is_fav']
            is_pinned = request.POST['is_pinned']

            # query maker and executor for all elements
            with transaction.atomic():
                for id in id_edit:
                    if id == '':
                        continue
                    # print('inside for')
                    query_edit = "Update {}\nSet".format(tablename)
                    # finding the corresponding index for the pk to edit items
                    index = -1
                    for ind in range(1, no_of_items + 1):
                        if request.POST['PrimKey_' + str(ind)] == id:
                            index = ind
                            break;
                    # found corresponding index, yes
                    query_cols = []  # puttigng different lines in list, then join by ,
                    for col in column_data:
                        # to do : for integers remove ' ' from 2nd {} || Done, added a loop
                        for meta in meta_data:
                            if meta[1] != col:
                                continue
                            if meta[2] == "TEXT":
                                query_cols.append("\n{} = '{}'".format(col, request.POST[col + "_" + str(index)]))
                            else:
                                # for numbers/ check pending
                                query_cols.append("\n{} = {}".format(col, request.POST[col + "_" + str(index)]))

                    query_temp = ','.join(query_cols)

                    query_edit += query_temp + "\n where \n {} = {};".format('PrimKey', id)

                    # To do : add try except block and turn auto commit off, for partial queries
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute(query_edit)
                    except:
                        return HttpResponse("Some Error Occured, the Data Was not saved")

            # print(id_delete)
            # query to delete stuff
            for id in id_delete:
                if id == '':
                    continue
                query_delete = "Delete from {} \n where PrimKey = {};".format(tablename, int(id))
                with connection.cursor() as cursor:
                    cursor.execute(query_delete)

            with connection.cursor() as cursor:
                cursor.execute("Select * from {};".format(tablename))
                row = cursor.fetchall()

            data = row
            no_of_items = len(data)
            indexing = range(1, len(data) + 1)
            mod = []
            # print(meta_data)
            columndata = ""
            for coldta in meta_data:
                columndata += coldta[1] + "$"

            columndata = columndata[:-1]
            for item in data:
                ls = []
                for element, meta in zip(item, meta_data):
                    tup = (str(element), meta[1], meta[2])
                    ls.append(tup)
                mod.append(ls)

            data = zip(indexing, mod)

            # updating fav and pinned status
            print("table check prior : ", is_table)
            tabl = is_table[0]
            # tabl = FolTabRel.objects.get(p_folder=folder, c_table=table, c_table_brief=table_brief, user=request.user, is_archived=False)
            print(tabl)

            tabl.is_fav = is_fav
            tabl.save()

            pinnedtableslist = FolTabRel.objects.filter(is_pinned='True')

            print("pinned tables are: ", len(pinnedtableslist))
            if len(pinnedtableslist) < 8:
                #     can add to pinned, else not
                tabl.is_pinned = is_pinned
            else:
                return HttpResponse("Pins Exceeded")

            tabl.save()

            return render(request, 'Users/view_set.html', {
                'table_meta': table_meta,
                'is_fav': is_fav,
                'is_pinned': is_pinned,
                'data': data,
                'meta_data': meta_data,
                'folder': fol,
                'column_data': columndata,
                'items_count': no_of_items,
                'table': table,
                'table_brief': table_brief,
            })

        if 'download-as-file' in request.POST:
            print("it is working properly broh")

        return HttpResponse("Yea boi")


def add_data_view(request, folder, table, table_brief):
    is_table = FolTabRel.objects.filter(p_folder=folder, c_table=table, c_table_brief=table_brief, user=request.user,
                                        is_archived=False)
    if len(is_table) == 0:
        return HttpResponse("Table Does not exists")

    fol = folder
    folder = folder.replace('-', '$').replace(' ', '_').replace("'", '_')
    tablename = request.user.username + "$$" + folder + "$$" + table
    with connection.cursor() as cursor:
        cursor.execute("Pragma table_info({})".format(tablename))
        meta_data = cursor.fetchall()
    table_meta = is_table[0].get_c_table()
    is_fav = is_table[0].is_table_fav()
    is_pinned = is_table[0].is_table_pinned()

    if request.method == 'GET':
        print("Method is get")
        return render(request, 'Users/add_data_in_set.html', {
            'table_meta': table_meta,
            'col_meta': meta_data,
            'table': table,
            'folder': fol,
            'table_brief': table_brief,
        })

    else:
        # method is post

        # irrespective of save exit or save add another, we need to add this value to the data base
        # metadata contans data about columns op la

        # query builder

        column_list = []
        data_list = []
        print(request.POST)
        for item in meta_data:
            print(item)
            if item[1] + '_data' in request.POST:
                print(item[1] + '_data')
                column_list.append(item[1])
                data_list.append("'" + request.POST[item[1] + '_data'] + "'")

        query = "Insert into {} {} values {};".format(tablename, "(" + ",".join(column_list) + ")",
                                                      "(" + ",".join(data_list) + ")")

        print("query is : ", query)
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
        except IntegrityError:
            return HttpResponse("Integrity Error. Cannot enter data")

        if 'save-exit' in request.POST:
            #  go back to view Page
            return redirect(view_set_view, fol, table, table_brief)

        if 'save-add' in request.POST:
            print("Save add another")
            return render(request, 'Users/add_data_in_set.html', {
                'table_meta': table_meta,
                'col_meta': meta_data,
                'table': table,
                'folder': fol,
                'table_brief': table_brief,
            })


def add_to_archive(request, folder, table, table_brief):
    is_table = FolTabRel.objects.filter(p_folder=folder, c_table=table, c_table_brief=table_brief, user=request.user,
                                        is_archived=False)
    if len(is_table) == 0:
        return HttpResponse("Table Does not exists")

    is_table = is_table[0]

    is_table.is_archived = True
    is_table.is_fav = False
    is_table.is_pinned = False
    is_table.save()

    return redirect(folder_view, folder)


def view_archive_view(request, folder):
    data = FolFolRel.objects.filter(p_folder=folder, user=request.user)
    table_data_raw = FolTabRel.objects.filter(p_folder=folder, user=request.user, is_archived=True)
    table_data = []
    tuplist = []

    for item in data:
        tuplist.append(item.get_c_folder())

    for item in table_data_raw:
        table_data.append(item.get_c_table())

    if request.method == 'POST':
        search_query = request.POST['seachBar']

        if search_query != '':
            tuplist = []
            table_data = []
            for item in data:
                if search_query in item.get_c_folder()[0]:
                    tuplist.append(item.get_c_folder())

            for item in table_data_raw:
                if search_query in item.get_c_folder()[0]:
                    table_data.append(item.get_c_table())

    url = ''
    folderlist = folder.split('-')
    urllist = []
    url = url + folderlist[0]
    tup = ()
    for item in folderlist:
        if item == url:
            tup = (item, url)
        else:
            url = url + '-' + item
            tup = (item, url)
            print(tup)
        urllist.append(tup)

    print(urllist)
    current = urllist[len(urllist) - 1]
    return render(request, 'Users/home.html', {
        'data': tuplist,
        'folder': folder,
        'urllist': urllist,
        'current': current,
        'table_data': table_data,
        'User': request.user.username,
        'is_archived': True,
        'is_dashboard': False,
        'is_favourite': False,
    })


def view_archiveset_view(request, folder, table, table_brief):
    is_table = FolTabRel.objects.filter(p_folder=folder, c_table=table, c_table_brief=table_brief, user=request.user
                                        , is_archived=True)
    print("Is table Check Before: ", is_table)
    if len(is_table) == 0:
        return HttpResponse("Table Does not exists, Table Brief is : {}".format(table_brief))
    fol = folder
    folder = folder.replace('-', '$').replace(' ', '_').replace("'", '_')
    tablename = request.user.username + "$$" + folder + "$$" + table
    table_meta = is_table[0].get_c_table()
    is_fav = is_table[0].is_table_fav()
    is_pinned = is_table[0].is_table_pinned()

    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("Pragma table_info({})".format(tablename))
            meta_data = cursor.fetchall()

        columndata = ""
        for coldta in meta_data:
            columndata += coldta[1] + "$"

        columndata = columndata[:-1]

        with connection.cursor() as cursor:
            cursor.execute("Select * from {};".format(tablename))
            row = cursor.fetchall()

        data = row
        no_of_items = len(data)
        indexing = range(1, len(data) + 1)
        mod = []

        for item in data:
            # print(item)
            ls = []
            for element, meta in zip(item, meta_data):
                # print(element, meta[1], meta[2])

                tup = (str(element), meta[1], meta[2])
                ls.append(tup)
            mod.append(ls)

        data = zip(indexing, mod)
        return render(request, 'Users/view_archived_set.html', {
            'table_meta': table_meta,
            'is_fav': is_fav,
            'is_pinned': is_pinned,
            'data': data,
            'meta_data': meta_data,
            'folder': fol,
            'column_data': columndata,
            'items_count': no_of_items,
            'table': table,
            'table_brief': table_brief,
        })
    else:
        tbl = is_table[0]
        if 'restore-button' in request.POST:
            tbl.is_archived = False
            tbl.save()
            return redirect(view_archive_view, fol)

        if 'delete-button' in request.POST:
            # delete table from sql table
            query = "DROP TABLE {};".format(tablename);
            with connection.cursor() as cursor:
                cursor.execute(query)

            # delete entry from folTabRel model
            to_del_table = FolTabRel.objects.filter(id=tbl.id)
            to_del_table.delete()
            return redirect(view_archive_view, fol)


def view_favourites_view(request, folder):
    data = FolFolRel.objects.filter(p_folder=folder, user=request.user)
    table_data_raw = FolTabRel.objects.filter(p_folder=folder, user=request.user, is_archived=False, is_fav=True)
    table_data = []
    tuplist = []

    for item in data:
        tuplist.append(item.get_c_folder())

    for item in table_data_raw:
        table_data.append(item.get_c_table())

    if request.method == 'POST':
        search_query = request.POST['seachBar']

        if search_query != '':
            tuplist = []
            table_data = []
            for item in data:
                if search_query in item.get_c_folder()[0]:
                    tuplist.append(item.get_c_folder())

            for item in table_data_raw:
                if search_query in item.get_c_folder()[0]:
                    table_data.append(item.get_c_table())

    url = ''
    folderlist = folder.split('-')
    urllist = []
    url = url + folderlist[0]
    tup = ()
    for item in folderlist:
        if item == url:
            tup = (item, url)
        else:
            url = url + '-' + item
            tup = (item, url)
            print(tup)
        urllist.append(tup)

    print(urllist)
    current = urllist[len(urllist) - 1]
    return render(request, 'Users/home.html', {
        'data': tuplist,
        'folder': folder,
        'urllist': urllist,
        'current': current,
        'table_data': table_data,
        'User': request.user.username,
        'is_archived': False,
        'is_dashboard': False,
        'is_favourite': True,
    })


def delete_folder(request, folder):
    # code to delete a whole folder from the dataset, deleting everything that comes in its way
    index = folder.rfind('-')
    if index == -1:
        index = 0

    # if index is 0, current folder is home, so parent folder wont exist, empty string
    parent_folder = folder[:index]
    child_folder = folder[index + 1:]
    print('Parent folder is : ', parent_folder)

    recursive_folder_delete(request, folder)
    if parent_folder != '':
        current_folder = FolFolRel.objects.get(user=request.user, p_folder=parent_folder, c_folder=child_folder)
        current_folder.delete()

    if parent_folder == '':
        parent_folder="Home"

    return redirect(folder_view, parent_folder)


def recursive_folder_delete(request, folder):
    # deleting tables present in current folder
    tables = FolTabRel.objects.filter(p_folder=folder, user=request.user)
    fol = folder
    folder = folder.replace('-', '$').replace(' ', '_').replace("'", '_')
    for table in tables:
        tablename = request.user.username + "$$" + folder + "$$" + table.c_table

        query = "DROP TABLE {};".format(tablename)
        with connection.cursor() as cursor:
            cursor.execute(query)

        table.delete()

    # deleting folders present in current folder

    folders = FolFolRel.objects.filter(p_folder=fol, user=request.user)

    for foldr in folders:
        next_folder = fol + "-" + foldr.c_folder
        recursive_folder_delete(request, next_folder)
        foldr.delete()
