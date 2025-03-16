class Repository:
    def __init__ (id,title):
        self.id = id
        self.title = title
    
    def __str__(self):
        return f"{self.id}({self.title})"
        
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #title = models.CharField(max_length=255, default='')
    #description = models.TextField(default='', blank=True, )
    #foreign_id = models.CharField(max_length=255, default='')
    #owner=models.ForeignKey(Developer, null=True, blank=True, related_name='repositories', on_delete=models.CASCADE)
    #parent=models.ForeignKey('self', null=True, blank=True, related_name='child', on_delete=models.SET_NULL)
    #software
    #watched_count=models.IntegerField(default=0)
    #stars_count=models.IntegerField(default=0)
    #loc = models.IntegerField(default=0)
    #files = models.IntegerField(default=0)
    #contributors
    #sponsors
    #commits
    #pr
    #created_at = AutoDateTimeField(default=timezone.now, editable=False)
    #updated_at = AutoDateTimeField(default=timezone.now, editable=False)