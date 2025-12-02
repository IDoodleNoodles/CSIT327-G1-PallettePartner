# Supabase Storage Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PallettePartner Application                  │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
         ┌──────────▼──────────┐   ┌─────────▼──────────┐
         │   Development       │   │   Production       │
         │   (Local Storage)   │   │ (Supabase Storage) │
         └──────────┬──────────┘   └─────────┬──────────┘
                    │                         │
         USE_SUPABASE_STORAGE=false   USE_SUPABASE_STORAGE=true
                    │                         │
         ┌──────────▼──────────┐   ┌─────────▼──────────────────┐
         │  Local File System  │   │  Supabase Storage Bucket   │
         │                     │   │  (S3-Compatible)           │
         │  media/             │   │                            │
         │  ├── avatars/       │   │  pallettepartner-media/    │
         │  ├── artworks/      │   │  ├── media/                │
         │  └── chat_images/   │   │  │   ├── avatars/          │
         │                     │   │  │   ├── artworks/         │
         │  static/            │   │  │   └── chat_images/      │
         │  ├── css/           │   │  └── static/               │
         │  ├── js/            │   │      ├── css/              │
         │  └── icon/          │   │      ├── js/               │
         └─────────────────────┘   │      └── icon/             │
                                   └────────────────────────────┘
```

## File Upload Flow

```
┌─────────────┐
│    User     │
│  (Browser)  │
└──────┬──────┘
       │ 1. Upload file
       │    (avatar/artwork/chat image)
       ▼
┌─────────────────────────────────────────┐
│          Django Application             │
│  ┌───────────────────────────────────┐  │
│  │   ImageField / FileField Model    │  │
│  └───────────────┬───────────────────┘  │
│                  │                       │
│  ┌───────────────▼───────────────────┐  │
│  │    Storage Backend Selection      │  │
│  │  (settings.DEFAULT_FILE_STORAGE)  │  │
│  └───────────────┬───────────────────┘  │
│                  │                       │
│    ┌─────────────┴─────────────┐        │
│    │                           │        │
│    ▼                           ▼        │
│ ┌─────────────┐       ┌──────────────┐ │
│ │   Local     │       │   Supabase   │ │
│ │   Storage   │       │   Storage    │ │
│ │   Backend   │       │   Backend    │ │
│ └──────┬──────┘       └──────┬───────┘ │
└────────┼─────────────────────┼─────────┘
         │                     │
         │                     │ 2. Upload via S3 API
         │                     ▼
         │          ┌────────────────────────┐
         │          │   Supabase Storage     │
         │          │   (S3-Compatible)      │
         │          │                        │
         │          │  - Bucket: pallette... │
         │          │  - Path: media/...     │
         │          │  - Public URL          │
         │          └────────┬───────────────┘
         │                   │
         │                   │ 3. Return public URL
         ▼                   ▼
   ┌──────────────────────────────────┐
   │        Database (PostgreSQL)      │
   │                                   │
   │  Profile.avatar = "URL"           │
   │  Artwork.image = "URL"            │
   │  Message.image = "URL"            │
   └──────────────────────────────────┘
              │
              │ 4. Template renders URL
              ▼
        ┌──────────────┐
        │   Browser    │
        │ <img src=""> │
        └──────────────┘
```

## Static Files Collection Flow

```
┌──────────────────────────────────────────┐
│   python manage.py collectstatic         │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│       Django Static Files Finder         │
│  - Collects from STATICFILES_DIRS        │
│  - Gathers app static files              │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│      STATICFILES_STORAGE Backend         │
│  (SupabaseStaticStorage or WhiteNoise)   │
└──────────────────┬───────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌───────────────┐   ┌──────────────────────┐
│   WhiteNoise  │   │  Supabase Storage    │
│   (Dev/Local) │   │  (Production)        │
│               │   │                      │
│  staticfiles/ │   │  bucket/static/      │
│  ├── css/     │   │  ├── css/            │
│  ├── js/      │   │  ├── js/             │
│  └── icon/    │   │  └── icon/           │
└───────────────┘   └──────────────────────┘
```

## Environment-Based Configuration

```
┌────────────────────────────────────────────────┐
│              settings.py                       │
├────────────────────────────────────────────────┤
│                                                │
│  USE_SUPABASE_STORAGE = os.getenv(...)        │
│                                                │
│  if USE_SUPABASE_STORAGE:                     │
│      ┌──────────────────────────────────┐     │
│      │  Production Configuration        │     │
│      │  ─────────────────────────       │     │
│      │  DEFAULT_FILE_STORAGE =          │     │
│      │    'SupabaseMediaStorage'        │     │
│      │                                  │     │
│      │  STATICFILES_STORAGE =           │     │
│      │    'SupabaseStaticStorage'       │     │
│      │                                  │     │
│      │  AWS_ACCESS_KEY_ID = ...         │     │
│      │  AWS_SECRET_ACCESS_KEY = ...     │     │
│      │  AWS_S3_ENDPOINT_URL = ...       │     │
│      │  AWS_STORAGE_BUCKET_NAME = ...   │     │
│      └──────────────────────────────────┘     │
│                                                │
│  else:                                        │
│      ┌──────────────────────────────────┐     │
│      │  Development Configuration       │     │
│      │  ────────────────────────         │     │
│      │  MEDIA_ROOT = BASE_DIR/'media'   │     │
│      │  STATIC_ROOT = .../'staticfiles' │     │
│      │                                  │     │
│      │  Uses local file system          │     │
│      │  WhiteNoise for static files     │     │
│      └──────────────────────────────────┘     │
│                                                │
└────────────────────────────────────────────────┘
```

## Storage Backend Classes

```
┌─────────────────────────────────────────────────────────┐
│  pallattepartner/pallate/storage.py                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────┐     │
│  │  class SupabaseMediaStorage(S3Boto3Storage)   │     │
│  │  ──────────────────────────────────────────   │     │
│  │  - bucket_name: pallettepartner-media         │     │
│  │  - location: 'media'                          │     │
│  │  - file_overwrite: False                      │     │
│  │  - custom_domain: Supabase public URL         │     │
│  │                                               │     │
│  │  Handles:                                     │     │
│  │    ✓ Avatar uploads                           │     │
│  │    ✓ Artwork uploads                          │     │
│  │    ✓ Chat image uploads                       │     │
│  └───────────────────────────────────────────────┘     │
│                                                         │
│  ┌───────────────────────────────────────────────┐     │
│  │  class SupabaseStaticStorage(S3Boto3Storage)  │     │
│  │  ──────────────────────────────────────────   │     │
│  │  - bucket_name: pallettepartner-media         │     │
│  │  - location: 'static'                         │     │
│  │  - file_overwrite: True                       │     │
│  │  - custom_domain: Supabase public URL         │     │
│  │                                               │     │
│  │  Handles:                                     │     │
│  │    ✓ CSS files                                │     │
│  │    ✓ JavaScript files                         │     │
│  │    ✓ Icon files (PNG)                         │     │
│  └───────────────────────────────────────────────┘     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Supabase Storage Bucket Structure

```
pallettepartner-media/  (Public Bucket)
│
├── media/  (User Uploads)
│   │
│   ├── avatars/
│   │   ├── default.png
│   │   ├── user_1_avatar_abc123.jpg
│   │   ├── user_2_avatar_def456.png
│   │   └── ...
│   │
│   ├── artworks/
│   │   ├── artwork_1_xyz789.jpg
│   │   ├── artwork_2_ghi012.png
│   │   └── ...
│   │
│   └── chat_images/
│       ├── message_1_jkl345.jpg
│       ├── message_2_mno678.png
│       └── ...
│
└── static/  (Collected Static Files)
    │
    ├── css/
    │   ├── loading.css
    │   └── pallate.css
    │
    ├── js/
    │   ├── animations.js
    │   ├── cards.js
    │   ├── chat.js
    │   ├── dashboard.js
    │   ├── favorites.js
    │   ├── filters.js
    │   ├── navigation.js
    │   ├── notifications.js
    │   ├── pallate.js
    │   ├── portfolio.js
    │   ├── timeline.js
    │   └── utils.js
    │
    └── icon/
        ├── artist_icon.png
        ├── back_icon.png
        ├── collabpost_icon.png
        ├── comment_icon.png
        ├── dashboard.png
        ├── favorite_icon.png
        ├── home_icon.png
        ├── message_icon.png
        ├── navigation_icon.png
        ├── notification_icon.png
        ├── profile_icon.png
        ├── search_icon.png
        ├── settings_icon.png
        ├── upload_artwork_icon.png
        └── upload_icon.png
```

## URL Resolution

### Development (Local)
```
Template:           {% static 'icon/dashboard.png' %}
Resolves to:        /static/icon/dashboard.png
Served from:        D:/project/static/icon/dashboard.png
```

### Production (Supabase)
```
Template:           {% static 'icon/dashboard.png' %}
Resolves to:        https://xxxxx.supabase.co/storage/v1/object/public/
                    pallettepartner-media/static/icon/dashboard.png
Served from:        Supabase Storage Bucket
```

### Media Files (Production)
```
Database:           Profile.avatar = "media/avatars/user_123.jpg"
Template:           {{ user.profile.avatar.url }}
Resolves to:        https://xxxxx.supabase.co/storage/v1/object/public/
                    pallettepartner-media/media/avatars/user_123.jpg
Served from:        Supabase Storage Bucket
```

## Access Control Flow

```
┌──────────────────────────────────────────────────────┐
│              Supabase Storage Policies               │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Policy 1: Public Read Access                       │
│  ┌────────────────────────────────────────────┐     │
│  │  SELECT on storage.objects                 │     │
│  │  USING (bucket_id = 'pallettepartner...')  │     │
│  │                                            │     │
│  │  → Anyone can view/download files          │     │
│  └────────────────────────────────────────────┘     │
│                                                      │
│  Policy 2: Authenticated Upload                     │
│  ┌────────────────────────────────────────────┐     │
│  │  INSERT on storage.objects                 │     │
│  │  WITH CHECK (bucket_id = '...' AND         │     │
│  │             auth.role() = 'authenticated') │     │
│  │                                            │     │
│  │  → Only logged-in users can upload         │     │
│  └────────────────────────────────────────────┘     │
│                                                      │
│  Policy 3: User Can Update Own Files                │
│  ┌────────────────────────────────────────────┐     │
│  │  UPDATE on storage.objects                 │     │
│  │  USING (bucket_id = '...' AND              │     │
│  │         auth.uid() = owner)                │     │
│  │                                            │     │
│  │  → Users can only modify their own files   │     │
│  └────────────────────────────────────────────┘     │
│                                                      │
│  Policy 4: User Can Delete Own Files                │
│  ┌────────────────────────────────────────────┐     │
│  │  DELETE on storage.objects                 │     │
│  │  USING (bucket_id = '...' AND              │     │
│  │         auth.uid() = owner)                │     │
│  │                                            │     │
│  │  → Users can only delete their own files   │     │
│  └────────────────────────────────────────────┘     │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## Security & Authentication

```
Django Application                     Supabase Storage
─────────────────                      ────────────────

User uploads file
     │
     ├─→ Django validates
     │   - File type
     │   - File size
     │   - User authentication
     │
     ├─→ Generate unique filename
     │   - Prevents overwriting
     │   - Adds timestamp/UUID
     │
     └─→ Upload via S3 API ─────────→ Supabase receives
         - AWS Access Key ID            │
         - AWS Secret Access Key        ├─→ Validates credentials
         - Signed request               │   - Checks access keys
                                        │   - Verifies signature
                                        │
                                        ├─→ Checks bucket policies
                                        │   - Public read?
                                        │   - User authenticated?
                                        │
                                        ├─→ Stores file
                                        │   - In bucket location
                                        │   - With metadata
                                        │
                                        └─→ Returns public URL
                                                │
     ┌──────────────────────────────────────────┘
     │
     └─→ Django saves URL to database
         - Profile.avatar = "URL"
         - Artwork.image = "URL"
```

## Benefits Summary

```
┌─────────────────────────────────────────────────────────────┐
│                   Why Use Supabase Storage?                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ Persistence                                             │
│     - Files survive app restarts                           │
│     - Not lost on redeployment                             │
│     - Ephemeral hosting-friendly                           │
│                                                             │
│  ✅ Scalability                                             │
│     - No local disk space limits                           │
│     - Multiple servers share storage                       │
│     - Auto-scaling ready                                   │
│                                                             │
│  ✅ Performance                                             │
│     - CDN integration possible                             │
│     - Parallel uploads/downloads                           │
│     - Built-in caching                                     │
│                                                             │
│  ✅ Reliability                                             │
│     - 99.9% uptime SLA                                     │
│     - Automatic backups                                    │
│     - Data redundancy                                      │
│                                                             │
│  ✅ Security                                                │
│     - S3-compatible encryption                             │
│     - Access control policies                              │
│     - Secure credential storage                            │
│                                                             │
│  ✅ Cost-Effective                                          │
│     - Free tier: 1 GB storage                              │
│     - Pay-as-you-go pricing                                │
│     - No infrastructure management                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Reference: File Paths

| Context | Avatar Path Example | URL Format |
|---------|---------------------|------------|
| **Development** | `media/avatars/user_1.jpg` | `/media/avatars/user_1.jpg` |
| **Production** | `media/avatars/user_1.jpg` | `https://xxx.supabase.co/storage/v1/object/public/pallettepartner-media/media/avatars/user_1.jpg` |

| Context | Icon Path Example | URL Format |
|---------|-------------------|------------|
| **Development** | `static/icon/dashboard.png` | `/static/icon/dashboard.png` |
| **Production** | `static/icon/dashboard.png` | `https://xxx.supabase.co/storage/v1/object/public/pallettepartner-media/static/icon/dashboard.png` |
