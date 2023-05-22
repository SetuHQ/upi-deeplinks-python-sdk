# Changelog

## [2.1.0] - 2023-05-22

-   Refund APIs now return 2 additional fields - `created_at` and `type`.
-   Refund API tests have been updated to reflect the simplified status values of `Created`, `Pending` and `Initiated`.

## [2.0.0] - 2022-07-19

### Breaking change

-   The batch status API has changed to a more generic status API, and the `batch_id` is no longer returned in the response.

## [1.1.1] - 2022-05-27

### Bug fixes

-   Make SetuAPIException accessible from package index

## [1.1.0] - 2022-05-27

### Bug fixes

-   Rename SDK import back to setu

## [1.0.0] - 2022-05-26

-   Major refactor of the SDK
