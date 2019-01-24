Model Architechture

Membership
    -slug
    -type(free, pro, enterprise)
    -price
    -stripe plan id

UserMembership
    -user                           (foreignkey to default user)
    -strip customer id
    -membership type                (foreignkey to Membership)

Subscription
    -user membership                (foreignkey to UserMembership)
    -strip subscription id           
    -active

Course
    -slug
    -title
    -description
    -allowed membership             (foreignkey to Membership)

Lesson
    -slug
    -title
    -Course                         (foreignKey to Course)
    -position
    -video
    -thumbnail