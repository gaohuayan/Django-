class PageInfo():
    def __init__(self, cur_page, total, per_page=10, show_page=11):
        self.cur_page = cur_page
        self.per_page = per_page
        self.total = total
        self.show_page = show_page

        a, b = divmod(self.total, self.per_page)
        if b:
            a = a + 1
        self.total_page = a  #### 总页数

    #### 获取起始索引
    def get_start(self):
        start = (self.cur_page - 1) * self.per_page
        return start

    #### 获取结束索引
    def get_end(self):
        return self.cur_page * self.per_page

    def get_page(self):

        half = (self.show_page - 1) // 2

        #### taotal_page = 5 < show_page = 11
        if self.total_page < self.show_page:
            begin = 1
            end = self.total_page
        else:
            #### 左边极值判断
            if self.cur_page - half <= 0:
                begin = 1
                # end = self.cur_page + half
                end = self.show_page
            #### 右边极值的判断
            elif self.cur_page + half > self.total_page:
                # begin =  self.cur_page - half
                begin = self.total_page - self.show_page + 1
                end = self.total_page  ### 31
            #### 正常页码判断
            else:
                begin = self.cur_page - half
                end = self.cur_page + half

        page_list = []
        if self.cur_page == 1:
            astr = "<li><a href='#' aria-label='Previous'><span aria-hidden='true'>&laquo;</span></a></li>"
        else:
            astr = "<li><a href='/custom/?cur_page=%s' aria-label='Previous'><span aria-hidden='true'>&laquo;</span></a></li>" % (
                        self.cur_page - 1)
        page_list.append(astr)

        for i in range(begin, end + 1):
            if self.cur_page == i:
                # astr = "<a style='display:inline-block; padding:5px;margin:5px;background-color:red;' href='/custom/?cur_page=%s'>%s</a>" % (i, i)
                astr = "<li class='active'><a href='/custom/?cur_page=%s'>%s</a></li>" % (i, i)
            else:
                # astr = "<a style='display:inline-block; padding:5px;margin:5px' href='/custom/?cur_page=%s'>%s</a>" % (i, i)
                astr = "<li><a href='/custom/?cur_page=%s'>%s</a></li>" % (i, i)
            page_list.append(astr)

        if self.cur_page == self.total_page:
            astr = "<li><a href='#' aria-label='Next'><span aria-hidden='true'>&raquo;</span></a></li>"
        else:
            astr = "<li><a href='/custom/?cur_page=%s' aria-label='Next'><span aria-hidden='true'>&raquo;</span></a></li>" % (
                        self.cur_page + 1)
        page_list.append(astr)

        s = " ".join(page_list)

        return s


def custom(request):
    cur_page = request.GET.get('cur_page')
    cur_page = int(cur_page)

    '''
    mysql:
       seelct * from userinfo limit 0, 10 
       seelct * from userinfo limit 10, 10 

       cur_page    start   show_page
          1          0     10
          2          10    10
          3          20    10
          n         (n-1)*10, 10
    limit (cur_page - 1) * show_page 
    '''
    # total = models.UserInfo.objects.count()
    total = models.UserInfo.objects.filter(id__lte=44).count()
    page = PageInfo(cur_page, total)
    start = page.get_start()
    end = page.get_end()

    ### cur_page = 1   start = 0   end = 10
    ### cur_page = 2   start = 10  end = 20
    ### cur_page = 3   start  =20  end = 30
    # user_list = models.UserInfo.objects.all()[start:end]
    user_list = models.UserInfo.objects.filter(id__lte=44)[start:end]

    return render(request, "custom.html", {"user_list": user_list, "page": page})