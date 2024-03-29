from django.db import models
import os


class Board(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    school = models.ForeignKey("school.School", on_delete=models.CASCADE)
    title = models.CharField(max_length=40, unique=True)
    type = models.CharField(
        max_length=8,
        choices=(("ALL", "모두 허용"), ("ANON", "익명 전용"), ("REAL", "실명 전용")),
        default="ALL",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    content = models.TextField()
    author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)
    like_users = models.ManyToManyField(
        "accounts.User", related_name="like_articles", blank=True
    )
    comment_count = models.IntegerField(default=0)
    is_anonymous = models.BooleanField(default=False)

    def like_user_add(self, user):
        self.like_users.add(user)
        self.like_count += 1
        self.save()

    def like_user_remove(self, user):
        self.like_users.remove(user)
        self.like_count -= 1
        self.save()

    def comment_count_add(self):
        self.comment_count += 1
        self.save()

    def comment_count_remove(self):
        self.comment_count -= 1
        self.save()

    def is_like_user(self, user):
        return self.like_users.filter(pk=user.pk).exists()

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return self.title


def article_photo_path(instance, filename):
    article_id = instance.article.id
    return os.path.join("article", str(article_id), filename.lower())


class ArticlePhoto(models.Model):
    article = models.ForeignKey(
        Article, related_name="photos", on_delete=models.CASCADE
    )
    photo = models.ImageField(upload_to="article_photos")
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    orientation = models.CharField(
        max_length=10,
        choices=(
            ("HORIZONTAL", "수평"),
            ("VERTICAL", "수직"),
            ("SQUARE", "정사각형"),
        ),
        default="HORIZONTAL",
    )

    def __str__(self):
        return self.article.title

    @property
    def photo_square(self):
        prev = os.path.splitext(self.photo.url)
        new_url = prev[0] + "_square" + prev[1]
        return new_url


class ArticleVote(models.Model):
    article = models.OneToOneField(
        Article, related_name="vote", on_delete=models.CASCADE
    )
    vote_count = models.IntegerField(default=0)


class ArticleVoteItem(models.Model):
    vote = models.ForeignKey(
        ArticleVote,
        related_name="votes",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=40)
    count = models.IntegerField(default=0)
    voted_users = models.ManyToManyField(
        "accounts.User", related_name="voted_votes", blank=True
    )

    def do_vote(self, user):
        if self.voted_users.filter(pk=user.pk).exists():
            return
        self.voted_users.add(user)
        self.count += 1
        self.vote.vote_count += 1
        self.vote.save()
        self.save()

    def cancel_vote(self, user):
        if self.voted_users.filter(pk=user.pk).exists():
            self.voted_users.remove(user)
            self.count -= 1
            self.vote.vote_count -= 1
            self.vote.save()
            self.save()

    def is_voted(self, user):
        return self.voted_users.filter(pk=user.pk).exists()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)
    like_users = models.ManyToManyField(
        "accounts.User", related_name="like_comments", blank=True
    )
    is_anonymous = models.BooleanField(default=False)
    anonymous_number = models.IntegerField()

    def like_user_add(self, user):
        self.like_users.add(user)
        self.like_count += 1
        self.save()

    def like_user_remove(self, user):
        self.like_users.remove(user)
        self.like_count -= 1
        self.save()

    def is_like_user(self, user):
        return self.like_users.filter(pk=user.pk).exists()

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return self.content


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    mention_user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="mention_replies",
        blank=True,
        null=True,
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)
    like_users = models.ManyToManyField(
        "accounts.User", related_name="like_replies", blank=True
    )
    is_anonymous = models.BooleanField(default=False)

    def like_user_add(self, user):
        self.like_users.add(user)
        self.like_count += 1
        self.save()

    def like_user_remove(self, user):
        self.like_users.remove(user)
        self.like_count -= 1
        self.save()

    def is_like_user(self, user):
        return self.like_users.filter(pk=user.pk).exists()

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return self.content
