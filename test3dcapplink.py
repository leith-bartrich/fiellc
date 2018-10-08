import fiepipe3dcoat.applink.standard

def main():
    models = []
    models.append(fiepipe3dcoat.applink.standard.Mesh(";"))
    outModel = fiepipe3dcoat.applink.standard.Mesh("c:\\Users\\leith\\Desktop\\testoutput2.3b")
    mode = fiepipe3dcoat.applink.standard.Mode(fiepipe3dcoat.applink.standard.Mode.MODE_3B)
    fiepipe3dcoat.applink.standard.StartRoundTrip(models, outModel, mode,[])

if __name__ == "__main__":
    main()