## Roles
### **Role Types**

`admin`
`maintainer`
`contributor`

### Admin

- Add / remove `maintainers` and `contributors`
- Has full CRUD on any issue
- Can delete project
  
### Maintainer
- Has full CRUD on any issue

### Contributor
- Can Create an issue
- Can only Update or Delete issue where they are the author


## Data Structures

### Project
```
{
    _id: ObjectId(),
    name: String,
    author_id: String,
    contibutors: Array,
}
```

### Webhooks
```
{
    _id: ObjectId(),
    project_name: String,
    name: String,
    url: String
    guild_id: Int,
    channel_id: Int,
    categories: Array
}
```

### User
```
{
    _id: ObjectId(),
    discord_id: String,
    projects: [project_name: project_role],
}
```

```
{
    _id: ObjectId(),
    name: String,
}
```

### Issue
```
{
    _id: ObjectId(),
    project_name: String,
    user_id: String,
    version: String,
    summary: String,
    description: String
    type: "bug" || "suggestion",
    category: String,
    priority: "low" || "medium" || "high",
    status: "reported" || "in-progress" || "won't-fix" || "completed",
    archived: Boolean,
    modlogs: {
        title: String,
        body: String,
    },
    media: {
        embed_source: String,
        general_url: String
    }
}
```

### Notification
```
{
    _id: ObjectId(),
    user_id: discord_user_id,
    project_name: String,
    link: String,
    is_read: Boolean,
    message: String,
    created_at: Datetime
    type: error | info | success
}
```

## Bot Commands

## /create-project
*Description*
Create a new project and add the message author as a contributor to the new project.
Associates the discord guild with a project_name

*Parameters*
`project_name`

*Returns*
new `project_name`

### /register-issue-feed
*Description*
Will create webhook for issue feed on the specified project to the channel the command is run in.

*Parameters*
`project_name`

*Returns*
new `webhook_id` (unclear if this is possible)


### /setup-project
*Description*
Creates a new project with message author as a contributor.
Creates a new channel with the specified project name.
Creates a webhook on the newly created channel for issue feed

*Parameters*
`project_name`

*Returns*
new `project_name`
new `channel_id`
new `webhook_id`


### /add-contributor
*Description*
Associates a contributor to a project and will provide additional access to issue site

*Parameters*
`project_name`
`user_id`

*Returns*
new `project_name`
new `channel_id`
new `webhook_id`