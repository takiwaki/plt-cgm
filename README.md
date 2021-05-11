# plt-cgm
Plot the result of continuous glucose monitoring by [freestyle libre](https://www.freestyle.abbott/)

## Proceadure

1. Save your data as `fsl.txt`.
2. Run the code `plt-cgm.py`.
3. You will find `total.png` and `yyyy-mm-dd.png`.

## Example

![Sample](/img/sample.png)

## Note

To estimate HbA1c from average blood glucose, following formula is used.  
HbA1c=averaged blood glucose/30+1.7
See [the reference page](http://koujiebe.blog95.fc2.com/blog-entry-838.html) for the details.
