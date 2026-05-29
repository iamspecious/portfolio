---
layout: default
title: "Cat API Documentation — GET /v1/images/search"
---

# GET /v1/images/search

The Cat API — Images Search endpoint.

---

## Overview

Returns a list of cat images matching the specified filters. Use this endpoint to retrieve random or ordered images, filter by breed or category, or page through a stable result set.

Unauthenticated requests return a single random image with no filtering or pagination. Authenticated requests unlock batch retrieval up to 25 results, breed and category filtering, and full pagination support.

---

## Authentication

The API uses key-based authentication passed as a request header.

| Header | Value |
|---|---|
| `x-api-key` | Your API key |

Get a free API key at [thecatapi.com](https://thecatapi.com).

**Authenticated vs unauthenticated behaviour:**

| | Unauthenticated | Authenticated |
|---|---|---|
| Max results per request | 1 | 25 |
| Filter by breed or category | No | Yes |
| Pagination | No | Yes |
| Monthly request limit | — | 10,000 (free) / 100,000 (premium) |

Unauthenticated requests always return exactly one random image regardless of the values passed to `limit` or `page`.

---

## Base URL and Method

```
GET https://api.thecatapi.com/v1/images/search
```

---

## Query Parameters

All parameters are optional.

| Parameter | Type | Required | Description | Default | Example |
|---|---|---|---|---|---|
| `limit` | integer | Optional | Number of results to return. Maximum `25`. Values above `1` require a valid API key. | `1` | `limit=10` |
| `page` | integer | Optional | Page offset for paginated results. Zero-indexed. Only applies when `order` is `ASC` or `DESC`. | `0` | `page=2` |
| `order` | string | Optional | Sort order for results. `RANDOM` disables pagination and ignores `page`. Accepted values: `RANDOM`, `ASC`, `DESC`. | `RANDOM` | `order=ASC` |
| `breed_ids` | string | Optional | Comma-separated breed IDs to filter by. Returns only images associated with the specified breeds. See [`GET /v1/breeds`](https://api.thecatapi.com/v1/breeds) for valid IDs. | — | `breed_ids=beng,abys` |
| `category_ids` | string | Optional | Comma-separated category IDs to filter by. See [`GET /v1/categories`](https://api.thecatapi.com/v1/categories) for valid IDs. | — | `category_ids=1,5` |
| `has_breeds` | integer | Optional | When set to `1`, returns only images that have breed data attached. | `0` | `has_breeds=1` |
| `mime_types` | string | Optional | Comma-separated list of image types to include. Accepted values: `jpg`, `png`, `gif`. | All types | `mime_types=jpg,png` |
| `size` | string | Optional | Image size variant to return. Accepted values: `thumb`, `small`, `med`, `full`. | `med` | `size=full` |
| `format` | string | Optional | Response format. `json` returns a JSON array. `src` returns the raw image directly. | `json` | `format=json` |

---

## Request Example

```bash
curl -X GET "https://api.thecatapi.com/v1/images/search?limit=5&has_breeds=1&breed_ids=beng&order=ASC&page=0" \
  -H "x-api-key: YOUR_API_KEY"
```

---

## Response Schema

The endpoint returns a JSON array. Each element is an image object.

### Image object

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique identifier for the image. |
| `url` | string | Direct URL to the image file. |
| `width` | integer | Image width in pixels. |
| `height` | integer | Image height in pixels. |
| `breeds` | array | Breed objects associated with this image. Empty array if no breeds are attached. Present when `has_breeds=1` or `breed_ids` is specified. |
| `categories` | array | Category objects associated with this image. Empty array if no categories are attached. |

### Breed object (within `breeds`)

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique breed identifier. |
| `name` | string | Breed name. |
| `description` | string | Summary description of the breed. |
| `temperament` | string | Comma-separated temperament traits. |
| `origin` | string | Country of origin. |
| `life_span` | string | Typical lifespan range, in years. |
| `wikipedia_url` | string | Wikipedia URL for this breed. |
| `reference_image_id` | string | ID of the canonical reference image for this breed. |

---

## Response Example

```json
[
  {
    "id": "O3btzLlsRf",
    "url": "https://cdn2.thecatapi.com/images/O3btzLlsRf.jpg",
    "width": 1200,
    "height": 800,
    "breeds": [
      {
        "id": "beng",
        "name": "Bengal",
        "description": "Bengals are a lot of fun to live with, but they're definitely not the cat for everyone, or for first-time cat owners. Extremely active, curious, and always alert, nothing escapes their attention.",
        "temperament": "Alert, Agile, Energetic, Demanding, Intelligent",
        "origin": "United States",
        "life_span": "12 - 15",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Bengal_(cat)",
        "reference_image_id": "O3btzLlsRf"
      }
    ],
    "categories": []
  }
]
```

---

## Error States

| Status | Meaning | Cause | Resolution |
|---|---|---|---|
| `400 Bad Request` | Invalid parameter value | A query parameter contains an unrecognised value (e.g. `order=NEWEST`). | Check parameter names and accepted values in the table above. |
| `401 Unauthorized` | Authentication failed | The `x-api-key` header is missing or contains an invalid key. | Confirm the header name is lowercase (`x-api-key`) and the value matches your dashboard key exactly. |
| `429 Too Many Requests` | Rate limit exceeded | Monthly request allowance has been exhausted. | Upgrade to a premium plan, or wait for the allowance to reset at the start of the next billing month. |
| `500 Internal Server Error` | Unexpected server error | An error on the API side unrelated to your request. | Retry with exponential backoff. If the issue persists, check [thecatapi.com](https://thecatapi.com) for service status. |

---

## Notes

**Pagination**

Pagination is only available when `order` is `ASC` or `DESC`. When `order=RANDOM` (the default), the `page` parameter is ignored and each request returns an independent random set.

When pagination is active, the response includes a `pagination-count` response header containing the total number of results matching your current query. Use this to calculate total pages:

```
total_pages = ceil(pagination-count / limit)
```

**Rate limits**

Free-tier accounts are limited to 10,000 requests per month. Premium accounts receive 100,000 requests per month. No per-second rate limit is documented; standard exponential backoff is recommended for high-volume usage.

**`format=src`**

When `format=src` is set, the API responds with the raw image file rather than a JSON body. This is useful for embedding a random cat image directly in an `<img>` tag or similar context. All other filtering parameters still apply.
