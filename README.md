## Data Structures

### Project
```
{
    _id: ObjectId(),
    name: String,
    author: ObjectId(),
    contibutors: List,
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
    channel_id: Int
    categories: List
}
```

### User
```
{
    _id: ObjectId(),
    name: String,
    discord_id: String,
    github: String,
    projects: List,
    roles: List
}
```

### Role
*Types*
`author`
`contributor`


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
    project_id: Int,
    user_id: String,
    version: String,
    summary: String,
    description: String
    type: "bug" || "suggestion",
    category: String,
    priority: "low" || "medium" || "high",
    status: "reported" || "in-progress" || "won't-fix" || "completed",
    archived: Boolean,
    modLogs: {
        title: String,
        body: String,
    },
    media: {
        embedSource: String,
        generalUrl: String
    }
}
```

## Bot Commands

## /create-project
*Description*
Create a new project and add the message author as a contributor to the new project.
Associates the discord guild with a project_id

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
new `webhook_id` (unclear if this is possible)


### /add-contributor
*Description*
Assosiates a contributor to a project and will provide additional access to issue site

*Parameters*
`project_name`
`user_id` (@'ed value)

*Returns*
new `project_name`
new `channel_id`
new `webhook_id` (unclear if this is possible)