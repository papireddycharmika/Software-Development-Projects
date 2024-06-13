class Polynomial:
    def __init__(self,coeff):
        self.coeff=coeff

    def __repr__(self):
        terms=[]
        for index,coef in enumerate(self.coeff):
            if coef!=0:
                if index==0:
                    terms.append(f"{coef}")
                elif index==1:
                    terms.append(f"{coef}*x")
                else:
                    terms.append(f"{coef}*x^{index}")
        if terms:
            return " + ".join(terms)
        else:
            return "0"

    def __add__(self,other):
        max_len=max(len(self.coeff),len(other.coeff))
        result=[0]*max_len
        for i in range(max_len):
            if i<len(self.coeff):
                result[i]+=self.coeff[i]
            if i<len(other.coeff):
                result[i]+=other.coeff[i]
        return Polynomial(result)

    def __sub__(self,other):
        max_len=max(len(self.coeff),len(other.coeff))
        result=[0]*max_len
        for i in range(max_len):
            if i<len(self.coeff):
                result[i]+=self.coeff[i]
            if i<len(other.coeff):
                result[i]-=other.coeff[i]
        return Polynomial(result)

    def __mul__(self,other):
        result=[0]*(len(self.coeff)+len(other.coeff)-1)
        for i,self_coef in enumerate(self.coeff):
            for j,other_coef in enumerate(other.coeff):
                result[i+j]+=self_coef*other_coef
        return Polynomial(result)

    def derivative(self):
        result=[i*self.coeff[i] for i in range(1,len(self.coeff))]
        return Polynomial(result)
    
    def __truediv__(self,other):
        divisor=other.coeff
        dividend=self.coeff[:]
        quotient=[]
        while len(dividend)>=len(divisor):
            ltc=dividend[-1]/divisor[-1]    #ltc-leading term coeff
            ltp=len(dividend)-len(divisor)  #ltp-leading term power
            quotient=[0]*ltp+[ltc]+quotient
            subtract_poly=Polynomial([0]*ltp+[ltc*c for c in divisor])
            dividend=(Polynomial(dividend)-subtract_poly).coeff
            while dividend and dividend[-1]==0:
                dividend.pop()
        return Polynomial(quotient), Polynomial(dividend)

    @classmethod
    def from_string(cls,polynomial_str):
        terms=polynomial_str.replace(" ", "").split("+")
        max_power=0
        parsed_terms=[]
        for term in terms:
            if "x" in term:
                if "^" in term and not term.startswith("x"):
                    if "*" not in term:
                        coef,power=1.0,term[-1]
                    else:
                        coef,power=term.split("*x^")
                        power=int(power)
                elif "*x" in term:
                    coef,waste=term.split("*x")
                    power=1
                elif term.startswith("x^"):
                    coef=1.0
                    power=int(term[2:])
                elif term.startswith("x"):
                    coef=1.0
                    power=1
                coef=float(coef)
            else:
                coef=float(term)
                power=0
            parsed_terms.append((power,coef))
            max_power=max(max_power,power)
        coefficients=[0]*(max_power+1)
        for power,coef in parsed_terms:
            coefficients[power]=coef
        return cls(coefficients)



import tkinter as tk
from tkinter import ttk
class PolyCalcApp:
    def __init__(self,root):
        self.root=root
        self.root.title("Polynomial Calculator")

        self.poly1_label=ttk.Label(root,text="Polynomial 1:")
        self.poly1_label.grid(row=0,column=0,padx=10,pady=10)
        self.poly1_entry=ttk.Entry(root,width=50)
        self.poly1_entry.grid(row=0,column=1,padx=10,pady=10)

        self.poly2_label=ttk.Label(root,text="Polynomial 2:")
        self.poly2_label.grid(row=1,column=0,padx=10,pady=10)
        self.poly2_entry=ttk.Entry(root,width=50)
        self.poly2_entry.grid(row=1,column=1,padx=10,pady=10)

        self.operation_label=ttk.Label(root,text="Operation:")
        self.operation_label.grid(row=2,column=0,padx=10,pady=10)
        self.operation_combo=ttk.Combobox(root,values=["Add","Subtract","Multiply","Divide","Derivative"],state="readonly")
        self.operation_combo.grid(row=2,column=1,padx=10,pady=10)
        self.operation_combo.current(0)

        self.calculate_button=ttk.Button(root,text="Calculate",command=self.calculate)
        self.calculate_button.grid(row=3,column=0,columnspan=2,pady=20)

        self.result_label=ttk.Label(root,text="Result:")
        self.result_label.grid(row=4,column=0,padx=10,pady=10)
        self.result_entry=ttk.Entry(root,width=50)
        self.result_entry.grid(row=4,column=1,padx=10,pady=10)
        self.result_entry.config(state='readonly')

    def calculate(self):
        poly1=Polynomial.from_string(self.poly1_entry.get())
        poly2_str=self.poly2_entry.get()
        operation=self.operation_combo.get()
        
        result=None
        
        if operation=="Add":
            if poly2_str:
                poly2=Polynomial.from_string(poly2_str)
                result=poly1+poly2
            else:
                result='Enter both polynomials'
        elif operation=="Subtract":
            if poly2_str:
                poly2=Polynomial.from_string(poly2_str)
                result=poly1-poly2
            else:
                result='Enter both polynomials'
        elif operation=="Multiply":
            if poly2_str:
                poly2=Polynomial.from_string(poly2_str)
                result=poly1*poly2
        elif operation=="Divide":
            if poly2_str:
                poly2=Polynomial.from_string(poly2_str)
                quotient,remainder=poly1/poly2
                result=f"Quotient: {quotient}, Remainder: {remainder}"
            else:
                result='Enter both polynomials'
        elif operation=="Derivative":
            result=poly1.derivative()
        if result is not None:
            self.result_entry.config(state='normal')
            self.result_entry.delete(0,tk.END)
            self.result_entry.insert(0,str(result))
            self.result_entry.config(state='readonly')

def main():
    root=tk.Tk()
    app=PolyCalcApp(root)
    root.mainloop()

if __name__=="__main__":
    main()
