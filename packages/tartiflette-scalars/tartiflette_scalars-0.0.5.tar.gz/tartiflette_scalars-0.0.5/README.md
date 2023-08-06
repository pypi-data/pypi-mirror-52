# some useful scalars

## Usage

```
from tartiflette import Scalar
from tartiflette_scalars import Json, ObjectId, AnyScalar

Scalar("Json")(Json) # gets anything

Scalar("AnyScalar")(AnyScalar) # infer the type, "2" becomes 2, "true" becomes True, etc.

Scalar("ObjectId")(ObjectId) # transform a 16 characters string into a bson.ObjectId

```
