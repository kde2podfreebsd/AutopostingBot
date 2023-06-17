from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .UserTestModel import *  # noqa

# from .SubPerDayModel import *  # noqa
# from .MentionModel import *  # noqa
# from .PostModel import *  # noqa
# from .ChannelModel import *  # noqa
