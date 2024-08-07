import Link from "next/link";
import SidebarItem from "./SidebarItems";
import SidebarLine from "./SidebarLine";

const Sidebar = () => {
    return (

         <div className="text-center pt-12 bg-gray-900 basis-4/12 lg:basis-3/12 2xl:basis-2/12 flex-col">

            {/* <SidebarLine/> */}

            <SidebarItem title="Home" link="/" />

            <SidebarItem title="Repositories" link="/repositories" />

            <SidebarItem title="Collectors" link="/collectors" />

            <SidebarItem title="Evaluators" link="/evaluators" />

            <SidebarItem title="Settings" link="/settings" />

            <SidebarLine/>

        </div>

    )
}

export default Sidebar;