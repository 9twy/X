from abc import ABC, abstractmethod

# Follower (Observer) Interface
class Follower(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def set_account(self, account):
        pass

# Concrete Follower (Observer) representing a User
class UserFollower(Follower):
    def __init__(self, username):
        self.username = username
        self._account = None

    def update(self):
        post = self._account.get_latest_post(self)
        if post:
            print(f"📲 {self.username} received notification: '{post}' from @{self._account.account_name}")
        else:
            print(f"{self.username} received no new posts.")

    def set_account(self, account):
        self._account = account

# Account (Subject) Interface
class Account(ABC):
    @abstractmethod
    def follow(self, follower):
        pass

    @abstractmethod
    def unfollow(self, follower):
        pass

    @abstractmethod
    def notify_followers(self):
        pass

    @abstractmethod
    def get_latest_post(self, follower):
        pass

# Concrete Account (Subject) representing an X Account
class XAccount(Account):
    def __init__(self, account_name):
        self.account_name = account_name
        self._followers = []
        self._latest_post = None
        self._changed = False

    def follow(self, follower):
        if follower not in self._followers:
            self._followers.append(follower)
            follower.set_account(self)
            print(f"{follower.username} is now following @{self.account_name}.")

    def unfollow(self, follower):
        if follower in self._followers:
            self._followers.remove(follower)
            print(f"{follower.username} has unfollowed @{self.account_name}.")

    def notify_followers(self):
        if not self._changed:
            return
        for follower in self._followers:
            follower.update()
        self._changed = False

    def get_latest_post(self, follower):
        return self._latest_post

    def post_update(self, message):
        print(f"\n@{self.account_name} posted: '{message}'")
        self._latest_post = message
        self._changed = True
        self.notify_followers()


if __name__ == "__main__":
    
    x_account = XAccount("TechNews")

    user1 = UserFollower("saeed alghamdi")
    user2 = UserFollower("abdullah ali")
    user3 = UserFollower("mohammed shaa")

    x_account.follow(user1)
    x_account.follow(user2)
    x_account.follow(user3)

    x_account.post_update("Breaking: New tech released today!")

    x_account.unfollow(user2)

    x_account.post_update("Update: Details on the new tech are now live on our website.")
